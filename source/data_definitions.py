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


key_value_types = (numba.types.unicode_type, VoxelType.class_type.instance_type)
voxel_type_dictionary_spec = [("voxel_types", numba.types.DictType(*key_value_types))]

@jitclass(voxel_type_dictionary_spec)
class VoxelTypeDictionary:

	def __init__(self):
		self.voxel_types = numba.typed.Dict.empty(*key_value_types)
		self.voxel_types["air"] = VoxelType()
