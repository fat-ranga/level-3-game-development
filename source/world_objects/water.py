from source.meshes.water_mesh import WaterMesh


class Water:
	def __init__(self, game):
		self.game = game
		self.mesh = WaterMesh(game)
	
	def render(self):
		self.mesh.render()
