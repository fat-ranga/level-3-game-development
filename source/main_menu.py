import moderngl as mgl
from typing import Tuple

from source.user_interface import *
import pygame as pg
from glm import *


class MainMenu:
	def __init__(self, game):
		self.game = game

		# UI elements are rendered in the order that
		# they are added to this list.
		self.ui_elements: list = []

		self.create_ui()

		self.rebuild_ui()  # todo temporary
		#self.rebuild_ui()

	def create_ui(self):
		self.background = TextureRect(self.game)
		self.background.name = "Background"
		self.background.texture_id = 5
		self.background.size_in_pixels = ivec2(1280, 720)
		self.ui_elements.append(self.background)

		self.title = TextureRect(self.game)
		self.title.name = "Title"
		self.title.anchor = vec2(0, 0.75)
		self.title.texture_id = 3
		self.title.size_in_pixels = ivec2(310, 64)
		self.ui_elements.append(self.title)

		self.exit_button = Button(self.game)
		self.exit_button.name = "ExitButton"
		self.exit_button.texture_id = 10
		self.exit_button.is_selected_texture_id = 11
		self.exit_button.size_in_pixels = ivec2(87, 27)
		self.exit_button.resize()
		self.ui_elements.append(self.exit_button)

		self.single_player_button = Button(self.game)
		self.single_player_button.name = "SingleplayerButton"
		self.single_player_button.texture_id = 8
		self.single_player_button.is_selected_texture_id = 9
		self.single_player_button.size_in_pixels = ivec2(87, 27)
		self.single_player_button.resize()
		self.ui_elements.append(self.single_player_button)

		self.settings_button = Button(self.game)
		self.settings_button.name = "SettingsButton"
		self.settings_button.texture_id = 13
		self.settings_button.is_selected_texture_id = 14
		self.settings_button.size_in_pixels = ivec2(87, 27)
		self.settings_button.resize()
		self.ui_elements.append(self.settings_button)

		self.cap_button = Button(self.game)
		self.cap_button.name = "CapButton"
		self.cap_button.texture_id = 13
		self.cap_button.is_selected_texture_id = 14
		self.cap_button.size_in_pixels = ivec2(120, 10)
		self.cap_button.resize()
		self.ui_elements.append(self.cap_button)

		self.menu_buttons_container = Control(self.game)
		self.ui_elements.append(self.menu_buttons_container)
		self.exit_button.parent = self.menu_buttons_container
		self.single_player_button.parent = self.menu_buttons_container
		self.cap_button.parent = self.menu_buttons_container
		self.settings_button.parent = self.menu_buttons_container

		offset: float = 0.0
		self.exit_button.offset = vec2(0, 0)

		offset += self.single_player_button.size.y + self.exit_button.size.y
		self.single_player_button.offset = vec2(0, offset)

		offset += self.cap_button.size.y + self.single_player_button.size.y
		self.cap_button.offset = vec2(0, offset)

		offset += self.settings_button.size.y + self.cap_button.size.y
		self.settings_button.offset = vec2(0, offset)


		# Set anchors within our container depending on how many elements are in there.
		#container_elements[0].anchor = vec2(0, 1)
		#print(container_elements[0].name)
		#container_elements[1].anchor = vec2(0, -1)
		#for i in range(len(container_elements)):
		#	container_elements[i].anchor = 1 - (i / len(container_elements))



	def update(self):
		# Check mouse position and stuff for button selection.
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = convert_pygame_screen_pos_to_moderngl_screen_pos(self.game, vec2(mouse_pos))

		# De-select everything first.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].is_mouse_position_in_bounds = False

		# If the mouse isn't visible, then don't try to select anything.
		if not self.game.mouse_visible:
			return

		# Find the first top-most element that the mouse fits in
		# and make that the selected one, ignoring everything underneath.
		for i in range(len(self.ui_elements)):
			# Move onto the next element if this one doesn't detect the mouse position.
			if not self.ui_elements[-i - 1].detects_mouse:
				continue
			# If we have something on top selected, make sure not to
			# select anything underneath by returning out of this loop.
			if self.ui_elements[-i - 1].check_if_mouse_in_bounds(mouse_pos):
				self.ui_elements[-i - 1].is_mouse_position_in_bounds = True
				return

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
		#self.menu_buttons_container.resize()
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		for i in range(len(self.ui_elements)):
			self.ui_elements[-i - 1].resize()

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
							return
						if self.ui_elements[-i - 1].name == "ExitButton":
							self.game.is_running = False
							return
