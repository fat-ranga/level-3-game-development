import moderngl as mgl
from source.world import World
from source.world_objects.voxel_marker import VoxelMarker
from source.world_objects.water import Water
from source.world_objects.clouds import Clouds
from source.user_interface import *


class Scene:
	def __init__(self, game, texture_ids, voxel_data):
		self.game = game
		self.world = World(self.game, texture_ids=texture_ids, voxel_data=voxel_data)
		self.voxel_marker = VoxelMarker(self.world.voxel_handler)
		self.water = Water(game)
		self.clouds = Clouds(game)

		self.ui_elements = []

		self.crosshair = TextureRect(game)
		self.crosshair.size = vec2(0.04, 0.04)
		self.ui_elements.append(self.crosshair)

		#self.title = TextureRect(game)
		#self.ui_elements.append(self.title)
		#self.test_button = TextureRect(game)
		#self.test_button.size = vec2(0.08, 0.08)
		#self.ui_elements.append(self.test_button)

		self.rebuild_ui() # todo temporary
		#self.test_button.parent = self.title
	
	def update(self):
		self.world.update()
		self.voxel_marker.update()
		self.clouds.update()
	
	def render(self):
		# Render chunks and stuff.
		self.world.render()
		
		# rendering without cull face
		self.game.ctx.disable(mgl.CULL_FACE)
		self.clouds.render()
		self.water.render()

		self.game.ctx.enable(mgl.CULL_FACE)
		
		# Render player's voxel selection marker.
		self.voxel_marker.render()

		self.game.ctx.disable(mgl.DEPTH_TEST)
		# Render UI.
		#self.game.shader_program.ui_quad["u_texture_0"] = 1
		#self.test_button.render()

		self.game.shader_program.ui_quad["u_texture_0"] = 4
		self.crosshair.render()

		#self.game.shader_program.ui_quad["u_texture_0"] = 3
		# self.title.render()

		self.game.ctx.enable(mgl.DEPTH_TEST)



	def rebuild_ui(self):
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].mesh.rebuild()