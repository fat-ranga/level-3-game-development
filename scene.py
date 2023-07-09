from settings import *
from meshes.quad_mesh import QuadMesh


class Scene:
	def __init__(self, game):
		self.game = game
		self.quad = QuadMesh(self.game)

	def update(self):
		pass

	def render(self):
		self.quad.render()