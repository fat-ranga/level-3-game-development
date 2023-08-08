from source.settings import *

class Frustum:
	def __init__(self, camera):
		self.cam: Camera = camera

		self.factor_y: float = 1.0 / math.cos(half_y := self.cam.v_fov * 0.5)
		self.tan_y: float = math.tan(half_y)

		self.factor_x: float = 1.0 / math.cos(half_x := self.cam.h_fov * 0.5)
		self.tan_x: float = math.tan(half_x)

	def update_factors(self):
		self.factor_y = 1.0 / math.cos(half_y := self.cam.v_fov * 0.5)
		self.tan_y = math.tan(half_y)

		self.factor_x = 1.0 / math.cos(half_x := self.cam.h_fov * 0.5)
		self.tan_x = math.tan(half_x)

	def is_on_frustum(self, chunk):
		# For culling chunks that aren't visible to the player.
		
		# Vector to sphere centre.
		sphere_vec = chunk.center - self.cam.position
		
		# Check if this sphere is outside the NEAR and FAR planes.
		sz = glm.dot(sphere_vec, self.cam.forward)
		if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
			return False
		
		# Outside the TOP and BOTTOM planes?
		sy = glm.dot(sphere_vec, self.cam.up)
		dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
		if not (-dist <= sy <= dist):
			return False
		
		# Outside the LEFT and RIGHT planes?
		sx = glm.dot(sphere_vec, self.cam.right)
		dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
		if not (-dist <= sx <= dist):
			return False
		
		return True
