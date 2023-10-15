import typing

from numba.experimental import jitclass
import numba.types
import numba
import json

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


item_spec = [("string_id", numba.types.string),
			 ("max_amount", numba.types.uint16),
			 ("name", numba.types.string),
			 ("is_solid", numba.types.boolean),
			 ("texture_ids", numba.types.List(numba.types.string)),
			 ("amount", numba.types.uint16)]


# Composition over inheritance type thing!
@jitclass(item_spec)
class ItemType:
	string_id = "default"
	
	max_amount = 64
	name = "Default"
	icon = "default"
	
	def __init__(self):
		self.amount = 1


class Gun:
	ammunition_type: str = "7.62"
	
	recoil_x_max: float = 1.0
	recoil_y_max: float = 1.0
	
	recoil_x_min: float = 0.0
	recoil_y_min: float = 0.0
	
	texture = None  # TODO: doom texture stuff
	
	def __init__(self):
		self.magazine: Magazine = None
		self.projectile_in_chamber: bool = False
	
	def fire(self):
		pass
	
	def reload(self):
		pass


class Magazine:
	ammunition_type: str = "7.62"
	max_ammo: int = 30
	
	def __init__(self):
		self.ammo: int = 0


voxel_key_value_types = (numba.types.unicode_type, VoxelType.class_type.instance_type)
voxel_string_id_key_value_types = (
numba.types.uint8, numba.types.unicode_type)  # 8-bit int because there can only be 256 different voxel types.
voxel_numeric_id_key_value_types = (numba.types.unicode_type, numba.types.uint8)

texture_id_key_value_types = (numba.types.unicode_type, numba.types.uint64)

item_key_value_types = (numba.types.unicode_type, ItemType.class_type.instance_type)
item_string_id_key_value_types = (numba.types.uint64, numba.types.unicode_type)

voxel_data_dictionary_spec = [("voxel", numba.types.DictType(*voxel_key_value_types)),
							  ("voxel_string_id", numba.types.DictType(*voxel_string_id_key_value_types)),
							  ("voxel_numeric_id", numba.types.DictType(*voxel_numeric_id_key_value_types)),
							  ("texture_id", numba.types.DictType(*texture_id_key_value_types)),
							  ("item", numba.types.DictType(*item_key_value_types))]


@jitclass(voxel_data_dictionary_spec)
class VoxelDataDictionary:
	def __init__(self):
		self.voxel = numba.typed.Dict.empty(*voxel_key_value_types)
		self.voxel_string_id = numba.typed.Dict.empty(*voxel_string_id_key_value_types)
		self.voxel_numeric_id = numba.typed.Dict.empty(*voxel_numeric_id_key_value_types)
		self.texture_id = numba.typed.Dict.empty(*texture_id_key_value_types)
		self.item = numba.typed.Dict.empty(*item_key_value_types)


def load_voxel_data(path: str, texture_ids):
	file = open(path)
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
		new_list: numba.types.List(numba.types.string) = ["grass_side", "grass_side", "grass_top", "dirt", "grass_side",
														  "grass_side"]
		new_list.clear()  # Delete the default values before appending new ones.
		for id in json_file_fr[item]["texture_ids"]:
			new_list.append(id)
		
		new_voxel_type.texture_ids = new_list
		data.voxel[item] = new_voxel_type
		
		data.voxel_string_id[numba.types.uint8(voxel_type_numeric_id)] = item
		data.voxel_numeric_id[item] = numba.types.uint8(voxel_type_numeric_id)
		
		voxel_type_numeric_id += 1
	
	for key in texture_ids:
		data.texture_id[key] = numba.types.uint64(texture_ids[key])
	
	return data


def load_items(path: str):
	pass  # TODO: component rather than inheritance?
