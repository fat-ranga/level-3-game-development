from source.meshes.quad_mesh import QuadMesh


class Water:
	def __init__(self, game):
		self.game = game
		self.mesh = QuadMesh(game)
	
	def render(self):
		self.mesh.render()
