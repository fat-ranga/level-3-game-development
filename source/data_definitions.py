from numba.experimental import jitclass
import numba.types

test_spec = [("cap", numba.types.int32)]
@jitclass(test_spec)
class Test:
	def __init__(self):
		self.cap = 17


block_type_spec = [("string_id", numba.types.string),
				   ("block_name", numba.types.string),
				   ("is_solid", numba.types.boolean),
				   ("texture_ids", numba.types.List(numba.types.string))]

@jitclass(block_type_spec)
class BlockType:
	def __init__(self):
		self.string_id = "air"
		self.block_name = "Air"
		self.is_solid = False
		self.texture_ids = ["grass_top","dirt","grass_side","grass_side","grass_side","grass_side"]
	# self.icon

