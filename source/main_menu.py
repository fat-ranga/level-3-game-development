import moderngl as mgl
from source.user_interface import *

class MainMenu:
	def __init__(self, game):
		self.game = game

		self.ui_elements = []

		self.title = TextureRect(game)
		self.title.size = vec2(0.5, 0.25)
		self.ui_elements.append(self.title)

		self.background = TextureRect(game)
		self.background.size = vec2(2, 1)
		self.ui_elements.append(self.background)

		self.test_button = TextureRect(game)
		self.test_button.size = vec2(0.08, 0.08)
		self.ui_elements.append(self.test_button)

		self.rebuild_ui()  # todo temporary

	def update(self):
		pass

	def render(self):
		self.game.ctx.disable(mgl.DEPTH_TEST)
		# Render UI.
		self.game.shader_program.ui_quad["u_texture_0"] = 5
		self.background.render()

		#self.game.shader_program.ui_quad["u_texture_0"] = 1
		#self.test_button.render()

		self.game.shader_program.ui_quad["u_texture_0"] = 3
		self.title.render()

		self.game.ctx.enable(mgl.DEPTH_TEST)

	def rebuild_ui(self):
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].mesh.rebuild()
