from source.settings import *
from source.data_definitions import *

from numba import typed, types, typeof
from numba import jit

@njit(cache=True)
def get_ao(local_pos, world_pos, world_voxels, plane):
	x, y, z = local_pos
	wx, wy, wz = world_pos

	if plane == 'Y':
		a = is_void((x    , y, z - 1), (wx    , wy, wz - 1), world_voxels)
		b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
		c = is_void((x - 1, y, z    ), (wx - 1, wy, wz    ), world_voxels)
		d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
		e = is_void((x    , y, z + 1), (wx    , wy, wz + 1), world_voxels)
		f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
		g = is_void((x + 1, y, z    ), (wx + 1, wy, wz    ), world_voxels)
		h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

	elif plane == 'X':
		a = is_void((x, y    , z - 1), (wx, wy    , wz - 1), world_voxels)
		b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
		c = is_void((x, y - 1, z    ), (wx, wy - 1, wz    ), world_voxels)
		d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
		e = is_void((x, y    , z + 1), (wx, wy    , wz + 1), world_voxels)
		f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
		g = is_void((x, y + 1, z    ), (wx, wy + 1, wz    ), world_voxels)
		h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

	else:  # Z plane
		a = is_void((x - 1, y    , z), (wx - 1, wy    , wz), world_voxels)
		b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
		c = is_void((x    , y - 1, z), (wx    , wy - 1, wz), world_voxels)
		d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
		e = is_void((x + 1, y    , z), (wx + 1, wy    , wz), world_voxels)
		f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
		g = is_void((x    , y + 1, z), (wx    , wy + 1, wz), world_voxels)
		h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

	ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
	return ao


@njit(cache=False)
def pack_data(x, y, z, texture_id, face_id, ao_id, flip_id):
	# x: 6bit  y: 6bit  z: 6bit  texture_id: 8bit  face_id: 3bit  ao_id: 2bit  flip_id: 1bit
	a, b, c, d, e, f, g = x, y, z, texture_id, face_id, ao_id, flip_id

	b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
	fg_bit = f_bit + g_bit
	efg_bit = e_bit + fg_bit
	defg_bit = d_bit + efg_bit
	cdefg_bit = c_bit + defg_bit
	bcdefg_bit = b_bit + cdefg_bit

	packed_data = (
			a << bcdefg_bit |
			b << cdefg_bit |
			c << defg_bit |
			d << efg_bit |
			e << fg_bit |
			f << g_bit | g
	)
	return packed_data


@njit(cache=True)
def get_chunk_index(world_voxel_pos):
	wx, wy, wz = world_voxel_pos
	cx = wx // CHUNK_SIZE
	cy = wy // CHUNK_SIZE
	cz = wz // CHUNK_SIZE
	if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
		return -1

	# TODO cache coherency
	index = cx + WORLD_W * cz + WORLD_AREA * cy
	return index


@njit(cache=True)
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
	chunk_index = get_chunk_index(world_voxel_pos)
	if chunk_index == -1:
		return False
	chunk_voxels = world_voxels[chunk_index]

	x, y, z = local_voxel_pos
	# TODO cache coherency
	voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

	if chunk_voxels[voxel_index]:
		return False
	return True


@njit(cache=True)
def add_data(vertex_data, index, *vertices):
	for vertex in vertices:
		vertex_data[index] = vertex
		index += 1
	return index


# We need to form a mesh of faces based on what voxels are visible to us.
@njit(cache=False)
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels, voxel_types: VoxelTypeDictionary):
	# The size of this array is based on the following:
	#
	# ARRAY_SIZE = CHUNK_VOL * NUM_VOXEL_VERTICES * NUM_VERTEX_ATTRIBUTES
	#
	# We have TODO vertex attributes: x, y, z, voxel_id, face_id
	#
	# Each of these attributes is stored as a single unsigned byte: 0-255.
	# Make sure the amount of bits in d_type matches that of the packed data.

	vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
	index = 0

	print(voxel_types.voxel_types["air"].is_solid)

	for x in range(CHUNK_SIZE):
		for y in range(CHUNK_SIZE):
			for z in range(CHUNK_SIZE):
				# TODO cache coherency
				voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
				texture_id = 1

				if not voxel_id:
					continue

				# voxel world position
				cx, cy, cz = chunk_pos
				wx = x + cx * CHUNK_SIZE
				wy = y + cy * CHUNK_SIZE
				wz = z + cz * CHUNK_SIZE

				# top face
				if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
					#if block_types.texture_ids[0] == "grass_top":
					#	texture_id = 11
					# get ao values
					ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y')
					# Determine whether to flip the triangles of a face based on the ambient
					# occlusion values, so that we don't get directional artifacts.
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]
					 
					# format: x, y, z, texture_id, face_id, ao_id, flip_id
					v0 = pack_data(x    , y + 1, z    , texture_id, 0, ao[0], flip_id)
					v1 = pack_data(x + 1, y + 1, z    , texture_id, 0, ao[1], flip_id)
					v2 = pack_data(x + 1, y + 1, z + 1, texture_id, 0, ao[2], flip_id)
					v3 = pack_data(x    , y + 1, z + 1, texture_id, 0, ao[3], flip_id)

					# When the ambient occlusion conditions are met, we flip the order
					# of triangles for this face, so we do not get anisotropic shading
					# on our ambient occlusion.
					if flip_id:
						index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
					else:
						index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

				# bottom face
				if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
					#if block_types.texture_ids[1] == "dirt":
					#	texture_id = 7
					ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]

					v0 = pack_data(x    , y, z    , texture_id, 1, ao[0], flip_id)
					v1 = pack_data(x + 1, y, z    , texture_id, 1, ao[1], flip_id)
					v2 = pack_data(x + 1, y, z + 1, texture_id, 1, ao[2], flip_id)
					v3 = pack_data(x    , y, z + 1, texture_id, 1, ao[3], flip_id)

					if flip_id:
						index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
					else:
						index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

				# right face
				if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
					#if block_types.texture_ids[2] == "grass_side":
					#	texture_id = 8
					ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]

					v0 = pack_data(x + 1, y    , z    , texture_id, 2, ao[0], flip_id)
					v1 = pack_data(x + 1, y + 1, z    , texture_id, 2, ao[1], flip_id)
					v2 = pack_data(x + 1, y + 1, z + 1, texture_id, 2, ao[2], flip_id)
					v3 = pack_data(x + 1, y    , z + 1, texture_id, 2, ao[3], flip_id)

					if flip_id:
						index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
					else:
						index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

				# left face
				if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
					#if block_types.texture_ids[3] == "grass_side":
					#	texture_id = 8
					#texture_id = 8
					ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]

					v0 = pack_data(x, y    , z    , texture_id, 3, ao[0], flip_id)
					v1 = pack_data(x, y + 1, z    , texture_id, 3, ao[1], flip_id)
					v2 = pack_data(x, y + 1, z + 1, texture_id, 3, ao[2], flip_id)
					v3 = pack_data(x, y    , z + 1, texture_id, 3, ao[3], flip_id)

					if flip_id:
						index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
					else:
						index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

				# back face
				if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
					#if block_types.texture_ids[4] == "grass_side":
					#	texture_id = 8
					ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]

					v0 = pack_data(x,     y,     z, texture_id, 4, ao[0], flip_id)
					v1 = pack_data(x,     y + 1, z, texture_id, 4, ao[1], flip_id)
					v2 = pack_data(x + 1, y + 1, z, texture_id, 4, ao[2], flip_id)
					v3 = pack_data(x + 1, y,     z, texture_id, 4, ao[3], flip_id)

					if flip_id:
						index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
					else:
						index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

				# front face
				if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
					#if block_types.texture_ids[5] == "grass_side":
					#	texture_id = 8

					ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')
					flip_id = ao[1] + ao[3] > ao[0] + ao[2]

					v0 = pack_data(x    , y    , z + 1, texture_id, 5, ao[0], flip_id)
					v1 = pack_data(x    , y + 1, z + 1, texture_id, 5, ao[1], flip_id)
					v2 = pack_data(x + 1, y + 1, z + 1, texture_id, 5, ao[2], flip_id)
					v3 = pack_data(x + 1, y    , z + 1, texture_id, 5, ao[3], flip_id)

					if flip_id:
						index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
					else:
						index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

	return vertex_data[:index + 1]
