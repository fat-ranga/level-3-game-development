from source.settings import *
from source.world_objects.chunk import Chunk
from source.voxel_handler import VoxelHandler
from source.data_definitions import *

import numba
from numba.typed import List
from numba.experimental import jitclass
import json
import numpy as np

class World:
	def __init__(self, game, texture_ids):
		self.game = game
		self.texture_ids = texture_ids
		self.voxel_data = self.load_voxel_data()
		# TODO: explain weird syntax
		self.chunks = [None for _ in range(WORLD_VOL)]

		# These are the actual voxels, all of our chunks only have a pointer to this.
		# dtype='uint8' means we store each voxel as an unsigned 8-bit integer, which
		# means we can have up to 256 different block types.
		self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
		self.build_chunks()
		self.build_chunk_mesh()
		self.voxel_handler = VoxelHandler(self)

	def load_voxel_data(self):

		file = open("data/voxel_types.json")
		json_file_fr = json.load(file)

		# Convert the untyped Python dictionary generated from the json file
		# to a typed dictionary of @jitclasses, since @njit functions cannot take in
		# variables that aren't typed, such as Python dictionaries.
		data = VoxelDataDictionary()

		voxel_type_numeric_id: numba.types.int8 = numba.types.uint8(0)

		for item in json_file_fr:
			new_voxel_type = VoxelType()

			new_voxel_type.string_id = item
			new_voxel_type.name = json_file_fr[item]["name"]
			new_voxel_type.is_solid = json_file_fr[item]["is_solid"]

			# TODO: fix this to not be a reflected list, since those are pending deprecation by the Numba library.
			# We have to make a new list because we cannot clear() the texture_ids list
			# from the VoxelType() class for some reason. So we set it to be a new one instead.

			# Can't make this list start off as empty, otherwise we get a memory footprint error or something.
			new_list: numba.types.List(numba.types.string) = ["grass_side", "grass_side", "grass_top", "dirt", "grass_side", "grass_side"]
			new_list.clear() # Delete the default values before appending new ones.
			for id in json_file_fr[item]["texture_ids"]:
				new_list.append(id)

			new_voxel_type.texture_ids = new_list
			data.voxel[item] = new_voxel_type

			data.voxel_string_id[numba.types.uint8(voxel_type_numeric_id)] = item
			data.voxel_numeric_id[item] = numba.types.uint8(voxel_type_numeric_id)

			voxel_type_numeric_id += 1

		for key in self.texture_ids:
			data.texture_id[key] = numba.types.uint64(self.texture_ids[key])

		#print(self.texture_ids)

		#print(data.texture_id)
		return data

	@njit
	def create_dict(self, items):
		return {k: v for k, v in items}

	def build_chunks(self):
		for x in range(WORLD_W):
			for y in range(WORLD_H):
				for z in range(WORLD_D):
					chunk = Chunk(self, position=(x, y, z))

					# TODO cache coherency
					# chunk_index = x * WORLD_W * WORLD_H + y * WORLD_D + z
					chunk_index = x + WORLD_W * z + WORLD_AREA * y
					self.chunks[chunk_index] = chunk

					# Put the chunk voxels into a separate array.
					self.voxels[chunk_index] = chunk.build_voxels()

					# Get pointer to voxels.
					chunk.voxels = self.voxels[chunk_index]

	def build_chunk_mesh(self):
		for chunk in self.chunks:
			chunk.build_mesh()

	def update(self):
		self.voxel_handler.update()

	def render(self):
		for chunk in self.chunks:
			chunk.render()
