import pygame as pg
import moderngl as mgl
from source.texture_atlas_packer import TextureAtlasPacker

class Textures:
	def __init__(self, game):
		self.game = game
		self.ctx = game.ctx
		self.atlas_packer = TextureAtlasPacker()
		
		# Load textures.
		self.texture_0 = self.load("ui/voxel_outline.png")
		self.texture_1 = self.load("water.png")
		self.texture_2 = self.load("ui/kiwicraft.png")
		self.texture_3 = self.load("ui/crosshair.png")
		
		# Make the atlas texture.
		self.texture_paths: list = self.atlas_packer.get_texture_paths_in_directory()
		self.texture_list: list = self.atlas_packer.load_textures(self.texture_paths)
		self.atlas_texture: pg.surface = self.load_texture(self.atlas_packer.pack_atlas(self.texture_list))
		
		# Assign texture unit.
		self.texture_0.use(location=0)
		self.atlas_texture.use(location=1)
		self.texture_1.use(location=2)
		self.texture_2.use(location=3)
		self.texture_3.use(location=4)
	
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
	def load(self, file_name):
		texture = pg.image.load(f"data/textures/{file_name}")
		texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

		texture = self.ctx.texture(
			size=texture.get_size(),
			components=4,
			data=pg.image.tostring(texture, "RGBA", False)
		)
		texture.anisotropy = 32.0
		texture.build_mipmaps()
		texture.filter = (mgl.NEAREST, mgl.NEAREST)
		return texture
