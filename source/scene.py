import moderngl as mgl
from source.world import World
from source.world_objects.voxel_marker import VoxelMarker
from source.world_objects.water import Water
from source.world_objects.clouds import Clouds
from source.world_objects.skybox import Skybox

from source.user_interface import *


class Scene:
	def __init__(self, game, texture_ids, voxel_data):
		self.game = game
		self.world = World(self.game, texture_ids=texture_ids, voxel_data=voxel_data)
		self.voxel_marker = VoxelMarker(self.world.voxel_handler)
		self.water = Water(game)
		self.clouds = Clouds(game)
		self.skybox = Skybox(game)

		self.ui_elements: list = []
		# Number of slots is dependent on player inventory size.
		self.create_inventory_ui()

		self.crosshair = TextureRect(game)
		self.crosshair.size_in_pixels = ivec2(128, 128)
		self.crosshair.scale = vec2(0.25, 0.25)
		self.crosshair.texture_id = 4
		self.ui_elements.append(self.crosshair)

		self.rebuild_ui() # todo temporary
	
	def update(self):
		self.world.update()
		self.voxel_marker.update()
		self.clouds.update()
		self.update_ui()
	
	def render(self):
		# Render chunks and stuff.
		self.world.render()

		# Render skybox after we have rendered all the other solid stuff,
		# such as the chunks. This means fewer fragments to fill for the GPU.
		self.skybox.render()
		
		# Disable backface culling, since we need to see both sides of water / clouds.
		self.game.ctx.disable(mgl.CULL_FACE)
		self.clouds.render()
		self.water.render()
		self.game.ctx.enable(mgl.CULL_FACE)
		
		# Render player's voxel selection marker.
		self.voxel_marker.render()

		# Disable depth-testing, since we are just drawing UI
		# elements on top of each other in screen-space.
		self.game.ctx.disable(mgl.DEPTH_TEST)
		# Render UI.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].update() # Update instead of render because element might be hidden.
		self.game.ctx.enable(mgl.DEPTH_TEST)

	def update_ui(self):
		update_ui_elements(self.game, self.ui_elements)

	def rebuild_ui(self):
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		resize_ui_elements(self.ui_elements)

	def create_inventory_ui(self):
		# Main inventory.
		for x in range(self.game.player.inventory.width):
			for y in range(self.game.player.inventory.height - 1):
				new_slot = Button(self.game)
				new_slot.size_in_pixels = ivec2(20, 20)
				new_slot.offset = vec2(x / 9, y / 9)
				new_slot.offset.x -= 0.45
				new_slot.scale = vec2(2, 2)
				new_slot.texture_id = 6
				new_slot.is_selected_texture_id = 12

				self.ui_elements.append(new_slot)

		# Toolbar.
		for x in range(self.game.player.inventory.width):
			new_slot = Button(self.game)
			new_slot.size_in_pixels = ivec2(20, 20)
			new_slot.offset = vec2(x / 9, 0.0)
			new_slot.anchor = vec2(0.0, -0.5)
			new_slot.scale = vec2(2, 2)
			new_slot.texture_id = 6
			new_slot.is_selected_texture_id = 12
			
			self.ui_elements.append(new_slot)
