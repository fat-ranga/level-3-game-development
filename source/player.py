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
		self.sprint_multiplier: float = 2.0

	def update(self):
		self.keyboard_control()
		self.mouse_control()
		self.handle_collision()

		self.position += self.velocity
		self.velocity = vec3(0, 0, 0) # todo: temporary

		super().update()  # Call camera update methods.

	# For when the player changes their FOV.
	def update_projection_matrix(self):
		self.m_proj = glm.perspective(self.game.settings.v_fov,
									  self.game.settings.aspect_ratio,
									  NEAR,
									  FAR)
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
			self.movement_direction += self.right # Todo: still according to local axis
		if key_state[pg.K_a]:  # Left.
			self.movement_direction -= self.right

		# Sprinting.
		if key_state[pg.K_LSHIFT]:
			self.movement_direction *= self.sprint_multiplier

		if key_state[pg.K_SPACE]:  # Up.
			self.movement_direction += vec3(0, 1, 0)

		if key_state[pg.K_LCTRL]:  # Down.
			self.movement_direction -= vec3(0, 1, 0)

		# Change velocity by our movement direction.
		self.movement_direction *= PLAYER_SPEED * self.game.delta_time

		self.velocity += self.movement_direction * 0.9
		self.velocity *= 0.75

	def handle_collision(self):
		overall_velocity_change = vec3(0, 0, 0)


		# Up and down.
		#velocity_change = self.collision_depenetration(vec3(0, 0.2, 0), "Y")
		#self.velocity.y += velocity_change
		velocity_change = self.collision_depenetration(vec3(0, -1.7, 0), "Y")
		print(velocity_change)
		self.velocity.y += velocity_change

		# Left (All of these directions are in world space).

		#velocity_change = self.collision_depenetration(vec3(-0.3, 0.2, 0), "X")
		#self.velocity.x += velocity_change
		#velocity_change = self.collision_depenetration(vec3(-0.3, -0.95, 0), "X") # In-between top and bottom.
		#self.velocity.x += velocity_change
		#velocity_change = self.collision_depenetration(vec3(-0.3, -1, 0), "X")
		#self.velocity.x += velocity_change
#
		## Right.
#
		#velocity_change = self.collision_depenetration(vec3(0.3, 0.2, 0), "X")
		#self.velocity.x += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0.3, -0.95, 0), "X")
		#self.velocity.x += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0.3, -1, 0), "X")
		#self.velocity.x += velocity_change
#
		## Back.
#
		#velocity_change = self.collision_depenetration(vec3(0, 0.2, 0.3), "Z")
		#self.velocity.z += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0, -0.95, 0.3), "Z")
		#self.velocity.z += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0, -1, 0.3), "Z")
		#self.velocity.z += velocity_change
#
		## Front.
#
		#velocity_change = self.collision_depenetration(vec3(0, 0.2, -0.3), "Z")
		#self.velocity.z += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0, -0.95, -0.3), "Z")
		#self.velocity.z += velocity_change
		#velocity_change = self.collision_depenetration(vec3(0, -1, -0.3), "Z")
		#self.velocity.z += velocity_change

		# Change the actual velocity.
		#self.velocity += overall_velocity_change

	def collision_depenetration(self, offset: vec3, axis: str) -> float:
		# Changes the player's velocity on a certain axis based on how far
		# their next position will penetrate into a solid voxel.

		# Calculate velocity next frame for only a single axis,
		# this is so that we can't phase through diagonal intersections
		# that don't have a voxel on the other side.
		# TODO: probably some way I could remove these checks and just pass in single axis instead
		if axis == "X":
			collision_position: vec3 = (self.position + self.velocity.x) + offset
		elif axis == "Y":
			collision_position: vec3 = (self.position + self.velocity.y) + offset
		elif axis == "Z":
			collision_position: vec3 = (self.position + self.velocity.z) + offset
		else:
			print("Collision De-penetration: Axis not specified.")
			return 0.0

		if self.collision(collision_position):
			# Since voxel_position is floored, we need to increase it by 1 if our
			# offset axis is negative, otherwise our velocity gets changed
			# by an extra metre.
			if axis == "X":
				collision_axis_position: float = collision_position.x
				voxel_position: int = int(collision_axis_position)
				if offset.x < 0:
					voxel_position += 1
			elif axis == "Y":
				collision_axis_position: float = collision_position.y
				voxel_position: int = int(collision_axis_position)
				if offset.y < 0:
					voxel_position += 1
			elif axis == "Z":
				collision_axis_position: float = collision_position.z
				voxel_position: int = int(collision_axis_position)
				if offset.z < 0:
					voxel_position += 1

			velocity_change: float = voxel_position - collision_axis_position

			print(f"voxel pos: {voxel_position}")
			print(f"collision pos delta v: {collision_position.x, collision_position.y, collision_position.z}")
			print(f"original pos: {self.position + offset}")

			return velocity_change
		else:
			print(f"voxel pos: {int(collision_position.y + 1)}")
			print(f"collision pos delta v: {collision_position}")
			print(f"original pos: {self.position + offset}")
			return 0.0

	def collision(self, position: vec3) -> bool:
		voxel_handler = self.game.scene.world.voxel_handler

		position: glm.ivec3 = glm.ivec3(position)

		# uint8
		voxel_id = voxel_handler.get_voxel_id(position)[0]  # First element is numeric ID.

		collision: bool = self.voxel_data.voxel[self.voxel_data.voxel_string_id[voxel_id]].is_solid

		return collision