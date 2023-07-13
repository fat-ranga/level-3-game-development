import pygame as pg
import moderngl as mgl
from source.texture_atlas_packer import TextureAtlasPacker

class Textures:
	def __init__(self, game):
		self.game = game
		self.ctx = game.ctx
		self.atlas_packer = TextureAtlasPacker()
		
		# load textures
		self.texture_0 = self.load('frame.png')
		self.texture_1 = self.load('water.png')
		self.texture_array_0 = self.load('tex_array_0.png', is_tex_array=True)
		
		# Make the atlas texture.
		self.texture_paths: list = self.atlas_packer.get_texture_paths_in_directory()
		self.texture_list: list = self.atlas_packer.load_textures(self.texture_paths)
		self.atlas_texture: pg.surface = self.load_texture(self.atlas_packer.pack_atlas(self.texture_list))
		
		# assign texture unit
		self.texture_0.use(location=0)
		self.atlas_texture.use(location=1)
		self.texture_1.use(location=2)
	
	def load_texture(self, texture):
		texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
		
		texture = self.ctx.texture(
			size=texture.get_size(),
			components=4,
			data=pg.image.tostring(texture, 'RGBA', False)
		)
		texture.anisotropy = 32.0
		texture.build_mipmaps()
		texture.filter = (mgl.NEAREST, mgl.NEAREST)
		return texture
	def load(self, file_name, is_tex_array=False):
		texture = pg.image.load(f'data/{file_name}')
		texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
		
		if is_tex_array:
			num_layers = 3 * texture.get_height() // texture.get_width()  # 3 textures per layer
			texture = self.game.ctx.texture_array(
				size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
				components=4,
				data=pg.image.tostring(texture, 'RGBA')
			)
		else:
			texture = self.ctx.texture(
				size=texture.get_size(),
				components=4,
				data=pg.image.tostring(texture, 'RGBA', False)
			)
		texture.anisotropy = 32.0
		texture.build_mipmaps()
		texture.filter = (mgl.NEAREST, mgl.NEAREST)
		return texture
