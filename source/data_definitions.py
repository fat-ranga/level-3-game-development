import typing

from numba.experimental import jitclass
import numba.types
import numba

test_spec = [("cap", numba.types.int32)]


@jitclass(test_spec)
class Test:
	def __init__(self):
		self.cap = 17


voxel_type_spec = [("string_id", numba.types.string),
				   ("name", numba.types.string),
				   ("is_solid", numba.types.boolean),
				   ("texture_ids", numba.types.List(numba.types.string))]


@jitclass(voxel_type_spec)
class VoxelType:
	def __init__(self):
		self.string_id = "air"
		self.name = "Air"
		self.is_solid = False
		self.texture_ids = ["grass_top", "dirt", "grass_side", "grass_side", "grass_side", "grass_side"]
		# self.icon


voxel_key_value_types = (numba.types.unicode_type, VoxelType.class_type.instance_type)
string_id_key_value_types = (numba.types.int8, numba.types.unicode_type) # 8-bit int because there can only be 256 different voxel types.

voxel_data_dictionary_spec = [("voxel", numba.types.DictType(*voxel_key_value_types)),
							  ("string_id", numba.types.DictType(*string_id_key_value_types))]

@jitclass(voxel_data_dictionary_spec)
class VoxelDataDictionary:

	def __init__(self):
		self.voxel = numba.typed.Dict.empty(*voxel_key_value_types)
		self.string_id = numba.typed.Dict.empty(*string_id_key_value_types)
