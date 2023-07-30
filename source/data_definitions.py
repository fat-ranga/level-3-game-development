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
		self.texture_ids = ["stone", "stone", "stone", "stone", "stone", "stone"]
	# self.icon


voxel_key_value_types = (numba.types.unicode_type, VoxelType.class_type.instance_type)
voxel_string_id_key_value_types = (
numba.types.uint8, numba.types.unicode_type)  # 8-bit int because there can only be 256 different voxel types.
voxel_numeric_id_key_value_types = (numba.types.unicode_type, numba.types.uint8)
texture_id_key_value_types = (numba.types.unicode_type, numba.types.uint64)

voxel_data_dictionary_spec = [("voxel", numba.types.DictType(*voxel_key_value_types)),
							  ("voxel_string_id", numba.types.DictType(*voxel_string_id_key_value_types)),
							  ("voxel_numeric_id", numba.types.DictType(*voxel_numeric_id_key_value_types)),
							  ("texture_id", numba.types.DictType(*texture_id_key_value_types))]


@jitclass(voxel_data_dictionary_spec)
class VoxelDataDictionary:

	def __init__(self):
		self.voxel = numba.typed.Dict.empty(*voxel_key_value_types)
		self.voxel_string_id = numba.typed.Dict.empty(*voxel_string_id_key_value_types)
		self.voxel_numeric_id = numba.typed.Dict.empty(*voxel_numeric_id_key_value_types)
		self.texture_id = numba.typed.Dict.empty(*texture_id_key_value_types)
