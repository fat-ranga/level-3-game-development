from settings import *
from meshes.base_mesh import BaseMesh


class QuadMesh(BaseMesh):
	def __init__(self, game):
		super().__init__()

		self.game = game
		self.ctx = game.ctx
		self.program = game.shader_program.quad

		# 3 floats per vertex co-ordinate, 3 floats per vertex colour.
		self.vbo_format = "3f 3f"
		self.attrs = ("in_position", "in_color")
		self.vao = self.get_vao()


	def get_vertex_data(self):
		vertices = [
		(0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0),
		(0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0)
		]

		colours = [
		(0, 1, 0), (1, 0, 0), (1, 1, 0),
		(0, 1, 0), (1, 1, 0), (0, 0, 1)
		]

		vertex_data = np.hstack([vertices, colours], dtype="float32")
		return vertex_data