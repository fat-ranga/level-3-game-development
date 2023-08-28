import moderngl as mgl
from typing import Tuple

from source.user_interface import *
import pygame as pg
from glm import *


class MainMenu:
	def __init__(self, game):
		self.game = game

		self.ui_elements = []

		self.background = TextureRect(game)
		self.background.texture_id = 5
		self.background.name = "Background"
		self.background.size_in_pixels = ivec2(1280, 720)
		self.ui_elements.append(self.background)

		self.title = TextureRect(game)
		self.title.position = vec2(0, 0.5)
		self.title.texture_id = 3
		self.title.name = "Title"
		self.title.size_in_pixels = ivec2(310, 64)
		self.ui_elements.append(self.title)

		self.singleplayer_button = Button(game)
		self.singleplayer_button.texture_id = 8
		self.singleplayer_button.is_selected_texture_id = 9
		self.singleplayer_button.name = "SingleplayerButton"
		self.singleplayer_button.size_in_pixels = ivec2(87, 27)
		self.ui_elements.append(self.singleplayer_button)

		self.exit_button = Button(game)
		self.exit_button.position = vec2(0, -0.25)
		self.exit_button.texture_id = 10
		self.exit_button.is_selected_texture_id = 11
		self.exit_button.name = "ExitButton"
		self.exit_button.size_in_pixels = ivec2(87, 27)
		self.ui_elements.append(self.exit_button)

		self.rebuild_ui()  # todo temporary

	def update(self):
		# Check mouse position and stuff for button selection.
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = convert_pg_screen_pos_to_moderngl_screen_pos(self.game, vec2(mouse_pos))

		for i in range(len(self.ui_elements)):
			self.ui_elements[i].check_if_mouse_in_bounds(mouse_pos)

	def render(self):
		# Disable Z depth testing, since we are not in 3D
		# and are just drawing things on top of each other.
		self.game.ctx.disable(mgl.DEPTH_TEST)

		# Render order is dependent on position in array.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].render()

		# Re-enable it for the rest of the rendering.
		self.game.ctx.enable(mgl.DEPTH_TEST)

	def rebuild_ui(self):
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].resize()

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONUP:
			if event.button == 3:
				print("right click released")
			if event.button == 1:
				for i in range(len(self.ui_elements)):
					# Sort through the list of UI elements backwards, so that
					# whatever's drawn on top gets the mouse input, and not whatever's
					# underneath.
					if self.ui_elements[-i - 1].is_mouse_position_in_bounds:
						# Determine what happens depending on the name of the UI element we just clicked.
						if self.ui_elements[-i - 1].name == "SingleplayerButton":
							self.game.start_game()
						if self.ui_elements[-i - 1].name == "ExitButton":
							self.game.is_running = False
							return
