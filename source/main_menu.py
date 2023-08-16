import moderngl as mgl
from source.user_interface import *
import pygame as pg
from glm import *

class MainMenu:
	def __init__(self, game):
		self.game = game

		self.ui_elements = []

		self.background = TextureRect(game)
		#self.background.size = vec2(2, 1)
		self.background.texture_id = 5
		self.background.name = "Background"
		self.background.size_in_pixels = ivec2(1280, 720)
		self.ui_elements.append(self.background)

		self.title = TextureRect(game)
		#self.title.size = vec2(0.5, 0.25)
		self.title.keep_aspect = False
		self.title.texture_id = 3
		self.title.name = "Title"
		self.title.size_in_pixels = ivec2(310, 64)
		self.ui_elements.append(self.title)

		self.test_button = TextureRect(game)
		#self.test_button.size = vec2(0.16, 0.16)
		self.test_button.texture_id = 6
		self.test_button.name = "Test Button"
		self.test_button.size_in_pixels = ivec2(18, 18)
		self.ui_elements.append(self.test_button)

		self.rebuild_ui()  # todo temporary

	def update(self):
		mouse_pos = vec2(pg.mouse.get_pos())

		mouse_pos.x /= self.game.settings.window_resolution.x
		mouse_pos.y /= self.game.settings.window_resolution.y

		mouse_pos.y = 1 - mouse_pos.y
		mouse_pos *= 2
		mouse_pos.x -= 1
		mouse_pos.y -= 1

		for i in range(len(self.ui_elements)):
			self.ui_elements[i].is_in_bounds(mouse_pos)

	def render(self):
		# Render order is dependent on position in array.
		self.game.ctx.disable(mgl.DEPTH_TEST)
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].render()

		# Render UI.
		#self.game.shader_program.ui_quad["u_texture_0"] = 5
		#self.background.render()

		##self.game.shader_program.ui_quad["u_texture_0"] = 1
		##self.test_button.render()

		#self.game.shader_program.ui_quad["u_texture_0"] = 3
		#self.title.render()

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
				print("left click released")