import glm
import pygame as pg
from source.camera import Camera
from source.settings import *
from glm import vec3
from source.data_definitions import *


class Player(Camera):
	def __init__(self, game, voxel_data, position=PLAYER_POS, yaw=-90, pitch=0):
		self.game = game
		self.voxel_data: VoxelDataDictionary = voxel_data

		# Initialise camera stuff.
		super().__init__(position,
						 yaw,
						 pitch,
						 self.game.settings.v_fov,
						 self.game.settings.h_fov,
						 self.game.settings.aspect_ratio)

		self.is_left_mouse_button_held: bool = False
		self.is_right_mouse_button_held: bool = False

		# Timer for breaking and placing voxels when mouse button is held down.
		self.max_change_voxel_timer = 10
		self.change_voxel_timer = self.max_change_voxel_timer

		# Movement stuff.
		self.movement_direction: vec3 = vec3()
		self.velocity: vec3 = vec3()
		self.gravity: vec3 = vec3(0, -9.81, 0)
		self.sprint_multiplier: float = 2.0
		self.dimensions = vec3(0.3, 1.9, 0.3)
		self.is_grounded: bool = False

	def update(self):
		self.apply_gravity() # Gravity first so that we can jump.
		self.keyboard_control()
		self.mouse_control()

		self.handle_collision()

		self.position += self.velocity

		#self.velocity = vec3(0, 0, 0)  # todo: temporary

		super().update()  # Call camera update methods.

	# For when the player changes their FOV.
	def update_projection_matrix(self):
		self.m_proj = glm.perspective(self.game.settings.v_fov,
									  self.game.settings.aspect_ratio,
									  NEAR,
									  FAR)

		# Update camera parameters so that chunks are only hidden outside of player frustum.
		self.h_fov = self.game.settings.h_fov
		self.v_fov = self.game.settings.v_fov
		self.aspect_ratio = self.game.settings.aspect_ratio
		self.frustum.update_factors()

	def handle_event(self, event):
		# Adding and removing voxels with mouse.
		# We break or place a voxel depending on the button pressed.
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 3:
				self.is_left_mouse_button_held: bool = True
				return
			if event.button == 1:
				self.is_right_mouse_button_held: bool = True
				return
		if event.type == pg.MOUSEBUTTONUP:
			if event.button == 3:
				self.is_left_mouse_button_held: bool = False
				return
			if event.button == 1:
				self.is_right_mouse_button_held: bool = False
				return

	def mouse_control(self):
		mouse_dx, mouse_dy = pg.mouse.get_rel()
		if mouse_dx:
			self.rotate_yaw(delta_x=mouse_dx * self.game.settings.mouse_sensitivity)
		if mouse_dy:
			self.rotate_pitch(delta_y=mouse_dy * self.game.settings.mouse_sensitivity)

		if not self.change_voxel_timer < 0:
			self.change_voxel_timer -= 1
			return

		if self.is_left_mouse_button_held:
			voxel_handler = self.game.scene.world.voxel_handler
			# We break or place a voxel depending on the button pressed.
			voxel_handler.set_voxel(3)
			self.change_voxel_timer = self.max_change_voxel_timer  # Reset the timer.
		if self.is_right_mouse_button_held:
			voxel_handler = self.game.scene.world.voxel_handler
			# We break or place a voxel depending on the button pressed.
			voxel_handler.set_voxel(1)
			self.change_voxel_timer = self.max_change_voxel_timer

	def keyboard_control(self):
		key_state = pg.key.get_pressed()
		self.movement_direction = vec3(0, 0, 0)

		# Calculate movement direction based on keyboard input.
		if key_state[pg.K_w]:  # Forwards.
			self.movement_direction += vec3(glm.cos(self.yaw), 0, glm.sin(self.yaw))
		if key_state[pg.K_s]:  # Backwards.
			self.movement_direction -= vec3(glm.cos(self.yaw), 0, glm.sin(self.yaw))

		if key_state[pg.K_d]:  # Right.
			self.movement_direction += self.right  # Todo: still according to local axis
		if key_state[pg.K_a]:  # Left.
			self.movement_direction -= self.right

		# Sprinting.
		if key_state[pg.K_LSHIFT]:
			self.movement_direction *= self.sprint_multiplier

		if key_state[pg.K_SPACE] and self.is_grounded:  # Up.
			self.movement_direction.y = 6.0
			#self.movement_direction += vec3(0, 1, 0) # todo flying creative mode state machine thing

		if key_state[pg.K_LCTRL]:  # Down.
			self.movement_direction -= vec3(0, 1, 0)

		# Change velocity by our movement direction.
		self.movement_direction *= PLAYER_SPEED * self.game.delta_time

		self.velocity += self.movement_direction * 0.2
		self.velocity.x *= 0.75
		self.velocity.z *= 0.75

	def apply_gravity(self):
		# Set downwards velocity to some small value.
		if self.is_grounded:
			self.velocity.y = -0.05
		# We are in the air and there is no support force, so our weight force is applied!
		else:
			self.velocity += self.gravity * 0.0008

	def handle_collision(self):
		overall_velocity_change = vec3(0, 0, 0)

		# Up and down.
		#collision_position = (self.position + self.velocity) + vec3(0, -1.7, 0)
		#if self.collision(collision_position):
		#	ranga = glm.ivec3(collision_position)
		#	velocity_change: glm.float64 = (ranga.y + 1) - collision_position.y
		#	self.velocity.y += velocity_change

		if (self.velocity.z > 0 and self.check_front()) or (self.velocity.z < 0 and self.check_back()):
			self.velocity.z = 0
		if (self.velocity.x > 0 and self.check_right()) or (self.velocity.x < 0 and self.check_left()):
			self.velocity.x = 0

		if self.velocity.y < 0:
			self.velocity.y = self.check_down_speed(self.velocity.y)
		elif self.velocity.y > 0:
			self.is_grounded: bool = False
			self.velocity.y = self.check_up_speed(self.velocity.y)


	def collision(self, position: vec3) -> bool:
		voxel_handler = self.game.scene.world.voxel_handler

		voxel_position: glm.ivec3 = glm.ivec3(position)

		# todo uint8
		voxel_id = voxel_handler.get_voxel_id(voxel_position)[0]  # First element is numeric ID.

		collision: bool = self.voxel_data.voxel[self.voxel_data.voxel_string_id[voxel_id]].is_solid

		return collision

	def check_up_speed(self, velocity):
		if self.collision(vec3(self.position.x - 0.3, self.position.y + 0.2 + velocity, self.position.z - 0.3)) and (not self.check_left() and not self.check_back()):
			return 0.0
		if self.collision(vec3(self.position.x + 0.3, self.position.y + 0.2 + velocity, self.position.z - 0.3)) and (not self.check_right() and not self.check_back()):
			return 0.0
		if self.collision(vec3(self.position.x - 0.3, self.position.y + 0.2 + velocity, self.position.z + 0.3)) and (not self.check_right() and not self.check_front()):
			return 0.0
		if self.collision(vec3(self.position.x + 0.3, self.position.y + 0.2 + velocity, self.position.z + 0.3)) and (not self.check_left() and not self.check_front()):
			return 0.0

		return velocity

	def check_down_speed(self, velocity):
		if self.collision(vec3(self.position.x - 0.3, self.position.y - 1.7 + velocity, self.position.z - 0.3)) and (not self.check_left() and not self.check_back()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x + 0.3, self.position.y - 1.7 + velocity, self.position.z - 0.3)) and (not self.check_right() and not self.check_back()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x - 0.3, self.position.y - 1.7 + velocity, self.position.z + 0.3)) and (not self.check_right() and not self.check_front()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x + 0.3, self.position.y - 1.7 + velocity, self.position.z + 0.3)) and (not self.check_left() and not self.check_front()):
			self.is_grounded = True
			return 0.0

		self.is_grounded = False
		return velocity

	def check_front(self) -> bool:
		if self.collision(vec3(self.position.x, self.position.y - 1.7, self.position.z + 0.3)):
			return True
		if self.collision(vec3(self.position.x, self.position.y + 0.2, self.position.z + 0.3)):
			return True

		return False

	def check_back(self) -> bool:
		if self.collision(vec3(self.position.x, self.position.y - 1.7, self.position.z - 0.3)):
			return True
		if self.collision(vec3(self.position.x, self.position.y + 0.2, self.position.z - 0.3)):
			return True

		return False

	def check_left(self) -> bool:
		if self.collision(vec3(self.position.x - 0.3, self.position.y - 1.7, self.position.z)):
			return True
		if self.collision(vec3(self.position.x - 0.3, self.position.y + 0.2, self.position.z)):
			return True

		return False

	def check_right(self) -> bool:
		if self.collision(vec3(self.position.x + 0.3, self.position.y - 1.7, self.position.z)):
			return True
		if self.collision(vec3(self.position.x + 0.3, self.position.y + 0.2, self.position.z)):
			return True

		return False