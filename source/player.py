import random
from glm import *
import pygame as pg

from source.camera import Camera
from source.settings import *
from source.data_definitions import *
from source.inventory import Inventory
from source.user_interface import show_ui_elements, hide_ui_elements, toggle_visibility_of_ui_elements


class Player(Camera):
	def __init__(self, game, voxel_data, position=PLAYER_POS, yaw=-90, pitch=0):
		self.game = game
		self.voxel_data: VoxelDataDictionary = voxel_data

		self.inventory = Inventory(ivec2(9, 4))
		self.is_inventory_hidden: bool = True

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
		self.max_change_voxel_timer: int = 10
		self.change_voxel_timer = self.max_change_voxel_timer

		# Movement stuff.
		self.movement_direction: vec3 = vec3()
		self.velocity: vec3 = vec3()
		self.gravity: vec3 = vec3(0, -9.81, 0)
		self.sprint_multiplier: float = 2.0

		# Collision bounding box dimensions.
		self.regular_dimensions = vec3(0.3, 1.9, 0.3)
		self.underwater_dimensions = vec3(0.3, 0.3, 0.3)
		self.dimensions = self.regular_dimensions

		# For positioning the head correctly.
		self.regular_dimensions_offset = vec3(0.0, 1.7, 0.0)
		self.underwater_dimensions_offset = vec3(0.0, 0.15, 0.0)
		self.dimensions_offset = self.regular_dimensions_offset

		self.is_grounded: bool = False
		self.is_swimming: bool = False

	def update(self):
		# Check if we're underwater.
		# TODO: make this a soft check in terms of gravity
		if self.position.y < WATER_LINE:
			self.is_swimming = True
		else:
			self.is_swimming = False

		self.mouse_control()
		self.keyboard_control()
		self.handle_collision()
		self.position += self.velocity

		#self.process_recoil()

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

	def create_ui(self):
		pass

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

		# print(self.game.settings.input_map["toggle_inventory"])
		if event.type == pg.KEYUP and event.key == pg.K_TAB:
			self.is_inventory_hidden = not self.is_inventory_hidden
			for i in range(len(self.game.scene.ui_elements)):
				self.game.scene.ui_elements[i].visible = self.is_inventory_hidden



	def mouse_control(self):
		# Get mouse movement.
		mouse_dx, mouse_dy = pg.mouse.get_rel()
		if mouse_dx:
			self.rotate_yaw(delta_x=mouse_dx * self.game.settings.mouse_sensitivity)
		if mouse_dy:
			self.rotate_pitch(delta_y=mouse_dy * self.game.settings.mouse_sensitivity)

		# Placing and breaking voxels timer.
		if not self.change_voxel_timer < 0:
			self.change_voxel_timer -= 1
			return

		# Place or break voxel.
		if self.is_left_mouse_button_held:
			voxel_handler = self.game.scene.world.voxel_handler
			# We break or place a voxel depending on the button pressed.
			voxel_handler.set_voxel(3)
			self.change_voxel_timer = self.max_change_voxel_timer  # Reset the timer.
		if self.is_right_mouse_button_held:
			voxel_handler = self.game.scene.world.voxel_handler
			# We break or place a voxel depending on the button pressed.
			ranga = voxel_handler.get_voxel_id(voxel_handler.voxel_world_pos)
			print(ranga[0])
			# TODO: check if we actually broke a block
			# and we need a way to convert the block id we get to a string id which we
			# can then compare against the items dictionary.
			voxel_handler.set_voxel(1)
			
			#gangster_item: Item = Item()
			#gangster_item.name = "Gangster"
			#gangster_item.string_id = "gangster"
			#self.inventory.add_item(gangster_item, 1)
			# TODO: Add item here usng voxel id of broken block
			
			self.change_voxel_timer = self.max_change_voxel_timer

	def shake_camera(self):
		print("shook cam au")
		ranga = (random.random() - 0.5) * 0.01
		cap = -random.random() * 0.01

		self.rotate_yaw(delta_x=ranga)
		self.rotate_pitch(delta_y=cap)

	def keyboard_control(self):
		# Calculate movement direction based on keyboard input.

		key_state = pg.key.get_pressed()
		self.movement_direction = vec3(0, 0, 0)

		if key_state[pg.K_g]:
			self.shake_camera()
		
		if key_state[pg.K_h]:
			hide_ui_elements(self.game.scene.main_inventory_ui_elements)
		
		if key_state[pg.K_j]:
			toggle_visibility_of_ui_elements(self.game.scene.inventory_hotbar_ui_elements)

		if self.is_swimming:
			self.movement_underwater(key_state)
		else:
			self.movement_regular(key_state)

	def movement_underwater(self, key_state):
		self.dimensions = self.underwater_dimensions
		self.dimensions_offset = self.underwater_dimensions_offset
		# Gravity is calculated first so that we can jump.
		# Set downwards velocity to some small value.
		#if self.is_grounded:
			#self.velocity.y = -0.001
		## We are in the air and there is no support force, so our weight force is applied!
		#else:
			#self.velocity += self.gravity * 0.0001

		if key_state[pg.K_w]:  # Forwards.
			self.movement_direction += self.forward
		if key_state[pg.K_s]:  # Backwards.
			self.movement_direction -= self.forward

		if key_state[pg.K_d]:  # Right.
			self.movement_direction += self.right
		if key_state[pg.K_a]:  # Left.
			self.movement_direction -= self.right

		if key_state[pg.K_SPACE]:  # Up.
			self.movement_direction.y += 1.0

		if key_state[pg.K_LCTRL]:  # Down.
			self.movement_direction.y += -1.0

		# Sprinting.
		if key_state[pg.K_LSHIFT]:
			self.movement_direction *= self.sprint_multiplier
		# Change velocity by our movement direction.
		self.movement_direction *= PLAYER_SPEED * self.game.delta_time

		self.velocity += self.movement_direction * 0.02
		self.velocity *= 0.95

	def movement_regular(self, key_state):
		self.dimensions = self.regular_dimensions
		self.dimensions_offset = self.regular_dimensions_offset

		# Gravity is decreased depending on how much of the player is submerged.
		# TODO: probably not right solution, the issue is the voxels not de-penetrating
		# the player when the collision shape changes size.
		diff = self.position.y - WATER_LINE
		amount_of_body_not_submerged: float = self.regular_dimensions_offset.y + diff
		if amount_of_body_not_submerged < 0.0:
			amount_of_body_not_submerged = 0.0
		if amount_of_body_not_submerged > 1.0:
			amount_of_body_not_submerged = 1.0

		# Gravity is calculated first so that we can jump.
		# Set downwards velocity to some small value.
		if self.is_grounded:
			self.velocity.y = -0.05
		# We are in the air and there is no support force, so our weight force is applied!
		else:
			self.velocity += self.gravity * 0.0008 * amount_of_body_not_submerged

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
		# self.movement_direction += vec3(0, 1, 0) # todo flying creative mode state machine thing

		if key_state[pg.K_LCTRL]:  # Down.
			self.movement_direction -= vec3(0, 1, 0)

		# Change velocity by our movement direction.
		self.movement_direction *= PLAYER_SPEED * self.game.delta_time

		self.velocity += self.movement_direction * 0.2
		self.velocity.x *= 0.75
		self.velocity.z *= 0.75

	def handle_collision(self):
		overall_velocity_change = vec3(0, 0, 0)

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

	# TODO: These if statements are all horrendously long and unreadable, should shorten them somehow
	def check_up_speed(self, velocity):
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y) + velocity, self.position.z - self.dimensions.x)) and (not self.check_left() and not self.check_back()):
			return 0.0
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y) + velocity, self.position.z - self.dimensions.x)) and (not self.check_right() and not self.check_back()):
			return 0.0
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y) + velocity, self.position.z + self.dimensions.x)) and (not self.check_right() and not self.check_front()):
			return 0.0
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y) + velocity, self.position.z + self.dimensions.x)) and (not self.check_left() and not self.check_front()):
			return 0.0

		return velocity

	def check_down_speed(self, velocity):
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y - self.dimensions_offset.y + velocity, self.position.z - self.dimensions.x)) and (not self.check_left() and not self.check_back()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y - self.dimensions_offset.y + velocity, self.position.z - self.dimensions.x)) and (not self.check_right() and not self.check_back()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y - self.dimensions_offset.y + velocity, self.position.z + self.dimensions.x)) and (not self.check_right() and not self.check_front()):
			self.is_grounded = True
			return 0.0
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y - self.dimensions_offset.y + velocity, self.position.z + self.dimensions.x)) and (not self.check_left() and not self.check_front()):
			self.is_grounded = True
			return 0.0

		self.is_grounded = False
		return velocity

	def check_front(self) -> bool:
		if self.collision(vec3(self.position.x, self.position.y - self.dimensions_offset.y, self.position.z + self.dimensions.x)):
			return True
		if self.collision(vec3(self.position.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y), self.position.z + self.dimensions.x)):
			return True

		return False

	def check_back(self) -> bool:
		if self.collision(vec3(self.position.x, self.position.y - self.dimensions_offset.y, self.position.z - self.dimensions.x)):
			return True
		if self.collision(vec3(self.position.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y), self.position.z - self.dimensions.x)):
			return True

		return False

	def check_left(self) -> bool:
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y - self.dimensions_offset.y, self.position.z)):
			return True
		if self.collision(vec3(self.position.x - self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y), self.position.z)):
			return True

		return False

	def check_right(self) -> bool:
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y - self.dimensions_offset.y, self.position.z)):
			return True
		if self.collision(vec3(self.position.x + self.dimensions.x, self.position.y + (self.dimensions.y - self.dimensions_offset.y), self.position.z)):
			return True

		return False