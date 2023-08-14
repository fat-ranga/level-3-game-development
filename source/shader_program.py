from source.settings import *


class ShaderProgram:
	def __init__(self, game):
		self.game = game
		self.ctx = game.ctx  # Pointer to OpenGL context so we can submit our shaders to it.
		self.player = game.player
		# -------- Put all the shaders we use in here -------- #
		self.chunk = self.get_program(shader_name="chunk")
		self.voxel_marker = self.get_program(shader_name="voxel_marker")
		self.water = self.get_program("water")
		self.clouds = self.get_program("clouds")
		self.ui_quad = self.get_program("ui_quad")
		# ------------------------- #
		self.set_uniforms_on_init()

	# For when the player changes their FOV.
	def update_projection_matrix(self):
		# chunk
		self.chunk["m_proj"].write(self.player.m_proj)
		# marker
		self.voxel_marker["m_proj"].write(self.player.m_proj)
		# water
		self.water["m_proj"].write(self.player.m_proj)
		# clouds
		self.clouds["m_proj"].write(self.player.m_proj)

	def set_uniforms_on_init(self):
		# chunk
		self.chunk["m_proj"].write(self.player.m_proj)
		self.chunk["m_model"].write(glm.mat4())
		self.chunk["atlas_texture"] = 1
		self.chunk["bg_color"].write(BG_COLOUR)
		self.chunk["water_line"] = WATER_LINE

		# marker
		self.voxel_marker["m_proj"].write(self.player.m_proj)
		self.voxel_marker["m_model"].write(glm.mat4())
		self.voxel_marker["u_texture_0"] = 0

		# water
		self.water["m_proj"].write(self.player.m_proj)
		self.water["u_texture_0"] = 2
		self.water["water_area"] = WATER_AREA
		self.water["water_line"] = WATER_LINE

		# clouds
		self.clouds["m_proj"].write(self.player.m_proj)
		self.clouds["center"] = CENTER_XZ
		self.clouds["bg_color"].write(BG_COLOUR)
		self.clouds["cloud_scale"] = CLOUD_SCALE

		# quad
		# TODO: need to be able to change uniforms between draw calls
		# Otherwise the texture is the same for every object that uses the same shader.
		self.ui_quad["u_texture_0"] = 4

	# self.ui_quad['m_proj'].write(self.player.m_proj)

	def update(self):
		# Update view matrices of objects, this transforms them
		# based on the camera's position.
		self.chunk["m_view"].write(self.player.m_view)
		self.voxel_marker["m_view"].write(self.player.m_view)
		self.water["m_view"].write(self.player.m_view)
		self.clouds["m_view"].write(self.player.m_view)

	# For loading shaders.
	def get_program(self, shader_name):
		with open(f"data/shaders/{shader_name}.vert") as file:
			vertex_shader = file.read()

		with open(f"data/shaders/{shader_name}.frag") as file:
			fragment_shader = file.read()

		program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
		return program
