from source.meshes.cloud_mesh import CloudMesh


class Clouds:
	def __init__(self, game):
		self.game = game
		self.mesh = CloudMesh(game)
	
	def update(self):
		self.mesh.program['u_time'] = self.game.time
	
	def render(self):
		self.mesh.render()
