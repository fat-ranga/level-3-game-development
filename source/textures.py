import pygame as pg
import moderngl as mgl
from source.texture_atlas_packer import TextureAtlasPacker

class Textures:
	def __init__(self, game):
		self.game = game
		self.ctx = game.ctx

		self.atlas_packer = TextureAtlasPacker()
		
		# Load textures.
		self.voxel_outline = self.load("ui/voxel_outline.png")
		self.water = self.load("water.png")
		self.kiwicraft = self.load("ui/kiwicraft.png")
		self.crosshair = self.load("ui/crosshair.png", filter=mgl.LINEAR)
		self.main_menu_background = self.load("ui/background.png")
		self.tile = self.load("ui/tile.png")
		self.skybox = self.load_texture_cube("skybox/", extension="png")
		self.singleplayer = self.load("ui/singleplayer.png")
		self.singleplayer_selected = self.load("ui/singleplayer_selected.png")
		self.exit = self.load("ui/exit.png")
		self.exit_selected = self.load("ui/exit_selected.png")
		
		# Make the atlas texture.
		self.texture_paths: list = self.atlas_packer.get_texture_paths_in_directory()
		self.texture_list: list = self.atlas_packer.load_textures(self.texture_paths)
		self.atlas_texture: pg.surface = self.load_texture(self.atlas_packer.pack_atlas(self.texture_list))
		
		# Assign texture unit.
		self.voxel_outline.use(location=0)
		self.atlas_texture.use(location=1)
		self.water.use(location=2)
		self.kiwicraft.use(location=3)
		self.crosshair.use(location=4)
		self.main_menu_background.use(location=5)
		self.tile.use(location=6)
		self.skybox.use(location=7)
		self.singleplayer.use(location=8)
		self.singleplayer_selected.use(location=9)
		self.exit.use(location=10)
		self.exit_selected.use(location=11)
	
	def load_texture(self, texture):
		# Texture is the wrong way round for some reason, so we have to flip it.
		texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
		
		texture = self.ctx.texture(
			size=texture.get_size(),
			components=4,
			data=pg.image.tostring(texture, "RGBA", False)
		)

		texture.filter = (mgl.NEAREST, mgl.NEAREST)
		return texture

	def load(self, file_name, filter=mgl.NEAREST):
		texture = pg.image.load(f"data/textures/{file_name}")
		texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

		texture = self.ctx.texture(
			size=texture.get_size(),
			components=4,
			data=pg.image.tostring(texture, "RGBA", False)
		)
		#texture.anisotropy = 32.0
		texture.build_mipmaps()
		texture.filter = (filter, filter)
		return texture

	def load_texture_cube(self, dir_path: str, extension="png"):
		# Flip back and front textures, otherwise the cube gets mapped incorrectly.
		faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
		textures = []
		for face in faces:
			#texture = pg.image.load(dir_path + f'{face}.{extension}').convert()
			texture = pg.image.load(f"data/textures/{dir_path}{face}.{extension}").convert()

			# The faces are correct from an outside view, but not inside.
			# So, we need to flip them.
			if face in ['right', 'left', 'front', 'back']:
				texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
			else:
				texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
			textures.append(texture)

		size = textures[0].get_size()
		texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

		for i in range(6):
			texture_data = pg.image.tostring(textures[i], 'RGB')
			texture_cube.write(face=i, data=texture_data)

		return texture_cube
