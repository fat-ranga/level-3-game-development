import pygame as pg
from source.camera import Camera
from source.settings import *


class Player(Camera):
	def __init__(self, game, position=PLAYER_POS, yaw=-90, pitch=0):
		self.game = game
		super().__init__(position, yaw, pitch) # Initialise camera stuff.
	
	def update(self):
		self.keyboard_control()
		self.mouse_control()
		super().update() # Call camera update methods.
	
	def handle_event(self, event):
		# Adding and removing voxels with mouse.
		if event.type == pg.MOUSEBUTTONDOWN:
			voxel_handler = self.game.scene.world.voxel_handler
			if event.button == 1:
				voxel_handler.set_voxel()
			if event.button == 3:
				voxel_handler.switch_mode()
	
	def mouse_control(self):
		mouse_dx, mouse_dy = pg.mouse.get_rel()
		if mouse_dx:
			self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
		if mouse_dy:
			self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
	
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
