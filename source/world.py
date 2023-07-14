from source.settings import *
from source.world_objects.chunk import Chunk
from source.voxel_handler import VoxelHandler


class World:
	def __init__(self, game):
		self.game = game
		# TODO: explain weird syntax
		self.chunks = [None for _ in range(WORLD_VOL)]
		
		# These are the actual voxels, all of our chunks only have a pointer to this.
		self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
		self.build_chunks()
		self.build_chunk_mesh()
		self.voxel_handler = VoxelHandler(self)
	
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