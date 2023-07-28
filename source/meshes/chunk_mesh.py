import json

from source.meshes.base_mesh import BaseMesh
from source.meshes.chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(BaseMesh):
	def __init__(self, chunk):
		# Initialise this mesh with a pointer to the chunk it is attached to.
		super().__init__()
		
		self.game = chunk.game
		self.chunk = chunk
		self.ctx = self.game.ctx
		self.program = self.game.shader_program.chunk
		self.block_types = chunk.block_types
		
		# Make sure to change the VBO format if new vertex attributes are added.
		self.vbo_format = "1u4"  # 1 unsigned 32-bit.
		self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())


		# MAKE SURE THERE IS A COMMA AFTER 'packed_data'!!!
		# TODO: fix this and the tuple in the parent class 'base_mesh'
		self.attrs: tuple = ("packed_data",)
		self.vao = self.get_vao()


	def rebuild(self):
		self.vao = self.get_vao()
	
	def get_vertex_data(self):
		mesh = build_chunk_mesh(
			chunk_voxels=self.chunk.voxels,
			format_size=self.format_size,
			chunk_pos=self.chunk.position,
			world_voxels=self.chunk.world.voxels,
			block_types=self.block_types
		)
		return mesh
