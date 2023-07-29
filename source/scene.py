import moderngl as mgl
from source.world import World
from source.world_objects.voxel_marker import VoxelMarker
from source.world_objects.water import Water
from source.world_objects.clouds import Clouds


class Scene:
	def __init__(self, game, texture_ids):
		self.game = game
		self.world = World(self.game, texture_ids=texture_ids)
		self.voxel_marker = VoxelMarker(self.world.voxel_handler)
		self.water = Water(game)
		self.clouds = Clouds(game)
	
	def update(self):
		self.world.update()
		self.voxel_marker.update()
		self.clouds.update()
	
	def render(self):
		# chunks rendering
		self.world.render()
		
		# rendering without cull face
		self.game.ctx.disable(mgl.CULL_FACE)
		self.clouds.render()
		self.water.render()
		self.game.ctx.enable(mgl.CULL_FACE)
		
		# voxel selection
		self.voxel_marker.render()
