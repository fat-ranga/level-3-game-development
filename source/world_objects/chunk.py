from source.meshes.chunk_mesh import ChunkMesh
from source.terrain_gen import *


class Chunk:
	def __init__(self, world, position):
		self.game = world.game
		self.world = world
		self.position = position
		self.m_model = self.get_model_matrix()
		self.voxels: np.array = None
		self.mesh: ChunkMesh = None
		self.is_empty = True
		self.voxel_types = world.voxel_types
		
		self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
		self.is_on_frustum = self.game.player.frustum.is_on_frustum
	
	def get_model_matrix(self):
		m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
		return m_model
	
	def set_uniform(self):
		self.mesh.program['m_model'].write(self.m_model)
	
	def build_mesh(self):
		self.mesh = ChunkMesh(self)
	
	def render(self):
		# So that we do not render chunks full of air.
		if not self.is_empty and self.is_on_frustum(self):
			self.set_uniform()
			self.mesh.render()
	
	def build_voxels(self):
		# Start the chunk as an empty, one-dimensional array of 8-bit numbers.
		voxels = np.zeros(CHUNK_VOL, dtype='uint8')
		
		# Determine the world co-ordinates of the chunks, relative to all voxels.
		# Using these, we can find the world co-ordinates of the current voxel.
		cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
		self.generate_terrain(voxels, cx, cy, cz)
		
		# Chunk is not empty if it has any voxel id apart from 0 (TODO change to air).
		if np.any(voxels):
			self.is_empty = False
		return voxels
	
	@staticmethod
	@njit(cache=True)
	def generate_terrain(voxels, cx, cy, cz):
		for x in range(CHUNK_SIZE):
			wx = x + cx
			for z in range(CHUNK_SIZE):
				wz = z + cz
				world_height = get_height(wx, wz)
				local_height = min(world_height - cy, CHUNK_SIZE)
				
				for y in range(local_height):
					wy = y + cy
					set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
