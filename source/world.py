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
	def __init__(self, game, texture_ids, voxel_data):
		self.game = game
		self.texture_ids = texture_ids
		self.voxel_data: VoxelDataDictionary = voxel_data
		# TODO: explain weird syntax
		self.chunks = [None for _ in range(WORLD_VOL)]

		# These are the actual voxels, all of our chunks only have a pointer to this.
		# dtype='uint8' means we store each voxel as an unsigned 8-bit integer, which
		# means we can have up to 256 different block types.
		self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype="uint8")
		self.build_chunks()
		self.build_chunk_mesh()
		self.voxel_handler = VoxelHandler(self)

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
