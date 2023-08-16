import moderngl as mgl
from source.user_interface import *
import pygame as pg
from glm import *


class MainMenu:
	def __init__(self, game):
		self.game = game

		self.ui_elements = []

		self.background = TextureRect(game)
		# self.background.size = vec2(2, 1)
		self.background.texture_id = 5
		self.background.name = "Background"
		self.background.size_in_pixels = ivec2(1280, 720)
		self.ui_elements.append(self.background)

		self.title = TextureRect(game)
		# self.title.size = vec2(0.5, 0.25)
		self.title.keep_aspect = False
		self.title.texture_id = 3
		self.title.name = "Title"
		self.title.size_in_pixels = ivec2(310, 64)
		self.ui_elements.append(self.title)

		self.test_button = TextureRect(game)
		# self.test_button.size = vec2(0.16, 0.16)
		self.test_button.texture_id = 6
		self.test_button.name = "Test Button"
		self.test_button.size_in_pixels = ivec2(18, 18)
		self.ui_elements.append(self.test_button)

		self.rebuild_ui()  # todo temporary

	def update(self):
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = self.convert_pg_screen_pos_to_moderngl_screen_pos(mouse_pos)

		for i in range(len(self.ui_elements)):
			self.ui_elements[i].check_if_mouse_in_bounds(mouse_pos)

	def convert_pg_screen_pos_to_moderngl_screen_pos(self, position: tuple[int, int]) -> vec2:
		# Precisely as the function says!
		position = vec2(position)

		# Normalise to 0 to 1 range.
		position.x /= self.game.settings.window_resolution.x
		position.y /= self.game.settings.window_resolution.y

		# Pygame: (0, 0) is top-left. (1, 1) is bottom-right.
		# ModernGL: (-1, 1) is top-left. (1, -1) is bottom-right.
		position.y = 1 - position.y
		position *= 2
		position.x -= 1
		position.y -= 1

		return position

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
						print(self.ui_elements[-i - 1].name)
						return
