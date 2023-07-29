from source.settings import *
import os
import sys
import pygame as pg

class TextureAtlasPacker:
	def __init__(self):
		
		self.texture_ids: dict = {}
		
		# Calculated during load_textures() based on the number of textures imported.
		self.texture_atlas_size_in_pixels: int = ATLAS_TEXTURE_ELEMENT_SIZE
		
		self.atlas_size_in_voxels: int
		
		#self.texture_paths: list = self.get_texture_paths_in_directory()
		#self.texture_list: list = self.load_textures(self.texture_paths)
		#self.atlas_texture = self.pack_atlas(self.texture_list)
		#print(self.texture_list)
	
	def get_texture_paths_in_directory(self, root_directory: str = DIR_TEXTURES) -> list:
		files: list = []
		
		# We get a double backslash if the file is in a subdirectory.
		# This is fine on Windows, hopefully os.walk() uses single forward slash
		# if this were to run on Linux.
		for root, subdir, files_in_dir, in os.walk(root_directory):
			for i in range(len(files_in_dir)):
				files.append(root + "/" + files_in_dir[i])
		
		#print("files: " + str(files))
		return files
	
	def load_textures(self, paths: list) -> list:
		image_list: list = []
		images_loaded: int = 0
		files_not_loaded: int = 0
		
		for texture_path in paths:
			# Get the last split in the string, which is the file extension.
			extension: str = texture_path.split(".")[-1]
			
			if extension.lower() != "png":
				files_not_loaded += 1
				print(f"Atlas Packer: {texture_path} not loaded to atlas: Texture not PNG.")
				continue
			
			texture = pg.image.load(texture_path)
			texture_size: tuple = texture.get_size()
			
			if texture_size != (ATLAS_TEXTURE_ELEMENT_SIZE, ATLAS_TEXTURE_ELEMENT_SIZE):
				files_not_loaded += 1
				print(f"Atlas Packer: {texture_path} not loaded to atlas: Incorrect size.")
				print(f"{texture_size} vs ({ATLAS_TEXTURE_ELEMENT_SIZE}, {ATLAS_TEXTURE_ELEMENT_SIZE})")
				continue
			
			# We have successfully loaded the image.
			image_list.append(texture)
			images_loaded += 1
			
			# Now we add the name of the file to TODO: finish
			file_name = os.path.basename(texture_path)
			# file_name = "cap." + "ranga." + file_name
			slice_count: int = len(file_name.split("."))
			file_slice_list: list = []
			
			# -1 removes the last slice, which is the file extension.
			for i in range(slice_count - 1):
				slice_string: str = file_name.split(".")[i]
				file_slice_list.append(slice_string)
			
			# Add back the full stop delimiter to get the original file name without the extension.
			self.texture_ids[".".join(file_slice_list)] = 0
		
		if images_loaded > 0: print(f"Atlas Packer: {images_loaded} textures successfully loaded to atlas.")
		if files_not_loaded > 0: print(f"Atlas Packer: {files_not_loaded} files not loaded to atlas.")
		
		# Make the atlas the smallest power of two it can be to fit all the textures.
		while (self.texture_atlas_size_in_pixels / ATLAS_TEXTURE_ELEMENT_SIZE) * (
				self.texture_atlas_size_in_pixels / ATLAS_TEXTURE_ELEMENT_SIZE) < len(image_list):
			self.texture_atlas_size_in_pixels *= 2
			
		return image_list
	
	def pack_atlas(self, textures: list) -> pg.surface:
		atlas_size_in_voxels = self.texture_atlas_size_in_pixels / ATLAS_TEXTURE_ELEMENT_SIZE
		
		width = self.texture_atlas_size_in_pixels
		height = self.texture_atlas_size_in_pixels
		texture_size: tuple = (width, height)
		
		atlas_texture: pg.surface = pg.Surface(texture_size)
		
		# We use a modulo operator to increment the row, which is why we start at -1 instead
		# of 0, otherwise the whole first row is skipped. We cannot put the modulo operation
		# at the end of the for loop to fix this because otherwise all textures in the first
		# y column (except the very first at (0, 0)) are skipped.
		current_row: int = -1
		colour: pg.color
		x_offset: int = 0
		y_offset: int = 0
		for t in range(len(textures)):
			# This strange-looking syntax assigns each texture in the texture_ids dictionary an ID, like this:
			# { "grass_top" : 3 , "coal_ore": 4, ... etc.}
			self.texture_ids[list(self.texture_ids.keys())[t]] = t
			
			# Move to the next row if we have reached the end of this one.
			if t % atlas_size_in_voxels == 0:
				current_row += 1
			
			x_offset = ATLAS_TEXTURE_ELEMENT_SIZE * t - (self.texture_atlas_size_in_pixels * current_row)
			y_offset = ATLAS_TEXTURE_ELEMENT_SIZE * current_row
			
			for x in range(ATLAS_TEXTURE_ELEMENT_SIZE):
				for y in range(ATLAS_TEXTURE_ELEMENT_SIZE):
					colour = textures[t].get_at((x, y))
					atlas_texture.set_at((int(x) + int(x_offset), int(y) + int(y_offset)), colour)
					
		#pg.image.save(atlas_texture, "data/atlas_texture.png")
		print(self.texture_ids)
		return atlas_texture