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

		self.ui_elements = []
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
		
		# rendering without cull face
		self.game.ctx.disable(mgl.CULL_FACE)
		self.clouds.render()
		self.water.render()

		self.game.ctx.enable(mgl.CULL_FACE)
		
		# Render player's voxel selection marker.
		self.voxel_marker.render()

		# Render skybox after everything else. This is more efficient
		# because everything else has been depth-tested first, and this means
		# fewer pixels to fill. TODO: what effect would this have on antialiasing?
		self.skybox.render()

		self.game.ctx.disable(mgl.DEPTH_TEST)

		# Render UI.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].render()

		self.game.ctx.enable(mgl.DEPTH_TEST)

	def update_ui(self):
		# Check mouse position and stuff for button selection.
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = convert_pg_screen_pos_to_moderngl_screen_pos(self.game, vec2(mouse_pos))

		for i in range(len(self.ui_elements)):
			self.ui_elements[i].check_if_mouse_in_bounds(mouse_pos)

	def rebuild_ui(self):
		# Called when the aspect ratio / window size is changed, resizes UI accordingly.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].resize()

	def create_inventory_ui(self):
		# Main inventory.
		for x in range(self.game.player.inventory.width):
			for y in range(self.game.player.inventory.height - 1):
				new_slot = Button(self.game)
				new_slot.size_in_pixels = ivec2(20, 20)
				new_slot.position = vec2(x / 20, y / 20)
				new_slot.scale = vec2(1, 1)
				new_slot.texture_id = 6
				new_slot.is_selected_texture_id = 12

				self.ui_elements.append(new_slot)

		# Toolbar.
		for x in range(self.game.player.inventory.width):
			new_slot = Button(self.game)
			new_slot.size_in_pixels = ivec2(20, 20)
			new_slot.position = vec2(x / 20, (y / 20) - 0.5)
			new_slot.scale = vec2(1, 1)
			new_slot.texture_id = 6
			new_slot.is_selected_texture_id = 12

			self.ui_elements.append(new_slot)
