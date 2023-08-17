from source.meshes.skybox_mesh import SkyBoxMesh


class Skybox:
	def __init__(self, game):
		self.game = game
		self.mesh = SkyBoxMesh(game)

	def render(self):
		self.mesh.render()
