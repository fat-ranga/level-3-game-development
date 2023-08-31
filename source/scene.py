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
			self.ui_elements[i].render()
		self.game.ctx.enable(mgl.DEPTH_TEST)

	def update_ui(self):
		# Check mouse position and stuff for button selection.
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = convert_pygame_screen_pos_to_moderngl_screen_pos(self.game, vec2(mouse_pos))

		# De-select everything first.
		for i in range(len(self.ui_elements)):
			self.ui_elements[i].is_mouse_position_in_bounds = False

		# If the mouse isn't visible, then don't try to select anything.
		if not self.game.mouse_visible:
			return

		# Find the first top-most element that the mouse fits in
		# and make that the selected one, ignoring everything underneath.
		for i in range(len(self.ui_elements)):
			# If we have something on top selected, make sure not to
			# select anything underneath by returning out of this loop.
			if self.ui_elements[-i - 1].check_if_mouse_in_bounds(mouse_pos):
				self.ui_elements[-i - 1].is_mouse_position_in_bounds = True
				return

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
				new_slot.anchor = vec2(x / 20, y / 20)
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
