import pygame as pg
from source.camera import Camera
from source.settings import *


class Player(Camera):
	def __init__(self, game, position=PLAYER_POS, yaw=-90, pitch=0):
		self.game = game
		super().__init__(position, yaw, pitch, self.game.settings.v_fov, self.game.settings.aspect_ratio) # Initialise camera stuff.

		self.is_left_mouse_button_held: bool = False
		self.is_right_mouse_button_held: bool = False

		self.max_change_voxel_timer = 10
		self.change_voxel_timer = self.max_change_voxel_timer

	
	def update(self):
		self.keyboard_control()
		self.mouse_control()
		super().update() # Call camera update methods.

	# For when the player changes their FOV.
	def update_projection_matrix(self):
		self.m_proj = glm.perspective(self.game.settings.v_fov, self.game.settings.aspect_ratio, NEAR, FAR)

	def handle_event(self, event):

		# Adding and removing voxels with mouse.
		#if event.type == pg.MOUSEBUTTONDOWN:
		#	voxel_handler = self.game.scene.world.voxel_handler
		#	# We break or place a voxel depending on the button pressed.
		#	voxel_handler.set_voxel(event.button)
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
			self.change_voxel_timer = self.max_change_voxel_timer # Reset the timer.
		if self.is_right_mouse_button_held:
			voxel_handler = self.game.scene.world.voxel_handler
			# We break or place a voxel depending on the button pressed.
			voxel_handler.set_voxel(1)
			self.change_voxel_timer = self.max_change_voxel_timer
	
	def keyboard_control(self):
		key_state = pg.key.get_pressed()
		vel = PLAYER_SPEED * self.game.delta_time
		if key_state[pg.K_w]:
			self.move_forward(vel)
		if key_state[pg.K_s]:
			self.move_back(vel)
		if key_state[pg.K_d]:
			self.move_right(vel)
		if key_state[pg.K_a]:
			self.move_left(vel)
		if key_state[pg.K_q]:
			self.move_up(vel)
		if key_state[pg.K_e]:
			self.move_down(vel)

