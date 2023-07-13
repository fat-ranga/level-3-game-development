from source.settings import *
from source.meshes.base_mesh import BaseMesh


class QuadMesh(BaseMesh):
	def __init__(self, game):
		super().__init__()
		self.game = game
		
		self.ctx = self.game.ctx
		self.program = self.game.shader_program.water
		self.vbo_format = '2u1 3u1'
		self.attrs = ('in_tex_coord', 'in_position')
		self.vao = self.get_vao()
	
	def get_vertex_data(self):
		vertices = np.array([
			(0, 0, 0), (1, 0, 1), (1, 0, 0),
			(0, 0, 0), (0, 0, 1), (1, 0, 1)
		], dtype='uint8')
		
		tex_coords = np.array([
			(0, 0), (1, 1), (1, 0),
			(0, 0), (0, 1), (1, 1)
		], dtype='uint8')
		
		vertex_data = np.hstack([tex_coords, vertices])
		return vertex_data
