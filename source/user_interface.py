from source.settings import *
import pygame as pg
from glm import vec2, ivec2
from source.meshes.ui_quad_mesh import QuadMesh


class Control:
	def __init__(self, game):
		self.game = game

		self.visible: bool = True
		self.keep_aspect: bool = True  # TODO x and y?
		self.name = "default"
		self.detects_mouse: bool = True
		self.is_mouse_position_in_bounds = False

		# All relative to the Control's bounding box.
		self.margin: vec2 = vec2(0.0, 0.0)
		self.anchor: vec2 = vec2(0.0, 0.0)  # (0,0) is centre of screen in ModernGL.
		self.scale: vec2 = vec2(2.0, 2.0)
		self.size_in_pixels: ivec2 = ivec2(0, 0)

		# Position value is determined from the other values, and is not used directly.
		self.position: vec2 = vec2(0.0, 0.0)  # Local position, relative to parent.
		# Size is also derived.
		self.size: vec2 = vec2(0.0, 0.0)
		self.parent: Control = None

	def resize(self):
		normalised_size_in_pixels: vec2 = vec2(self.size_in_pixels.x / self.game.settings.window_resolution.x,
											   self.size_in_pixels.y / self.game.settings.window_resolution.y)
		self.size = normalised_size_in_pixels * self.scale
		if not self.keep_aspect:
			self.size.x *= self.game.settings.aspect_ratio

		if self.parent:
			print(self.name)
			local_anchor = self.anchor * self.parent.size
			print(f"parentsize{self.parent.size}")

			# Scale first...
			offset_from_edges = self.anchor * self.size
			self.position = local_anchor - offset_from_edges

			# Then translate.
			self.position += self.parent.position
			#print(self.position)
		else:
			offset_from_edges = self.anchor * self.size
			self.position = self.anchor - offset_from_edges

	def update(self):
		if not self.visible:
			return

		self.render()

	def check_if_mouse_in_bounds(self, target_position: vec2) -> bool:
		if target_position.x < self.position.x - self.size.x:
			return False
		if target_position.x > self.position.x + self.size.x:
			return False
		if target_position.y < self.position.y - self.size.y:
			return False
		if target_position.y > self.position.y + self.size.y:
			return False

		return True

	def render(self):
		pass


class TextureRect(Control):
	def __init__(self, game):
		super().__init__(game)
		self.game = game
		self.texture_id: int = 0
		self.mesh = QuadMesh(self)

	def resize(self):
		super().resize()
		self.mesh.rebuild()

	def render(self):
		self.game.shader_program.ui_quad["u_texture_0"] = self.texture_id
		self.mesh.render()


class Button(Control):
	def __init__(self, game):
		super().__init__(game)
		self.texture_id: int = 0
		self.game = game
		self.is_selected: bool = False
		self.is_selected_texture_id: int = self.texture_id
		self.mesh = QuadMesh(self)

	def render(self):
		if self.is_mouse_position_in_bounds:
			self.is_selected = True
		else:
			self.is_selected = False

		if self.is_selected:
			self.game.shader_program.ui_quad["u_texture_0"] = self.is_selected_texture_id
		else:
			self.game.shader_program.ui_quad["u_texture_0"] = self.texture_id

		self.mesh.render()

	def resize(self):
		super().resize()
		self.mesh.rebuild()


class VBoxContainer(Control):
	def __init__(self, game):
		super().__init__(game)
		self.detects_mouse = False
		self.container_elements: list = []

	def resize(self):
		super().resize()
		self.size_in_pixels = ivec2(0, 0)
		largest_x_size: float = 0.0
		for i in range(len(self.container_elements)):
			self.container_elements[i].parent = self
			self.size_in_pixels.y += self.container_elements[i].size_in_pixels.y

			if self.container_elements[i].size_in_pixels.x > largest_x_size:
				largest_x_size = self.container_elements[i].size_in_pixels.x

		self.size_in_pixels.x = largest_x_size
		
		number_of_ui_elements: int = len(self.container_elements)
		
		for i in range(number_of_ui_elements):
			#y_position: float = 1 - (i * (2 / number_of_ui_elements))
			y_position: float = 1 - (i / 1.5) # TODO 1.5 might be y size
			
			self.container_elements[i].anchor = vec2(0, y_position)
			
		#self.container_elements[0].anchor = vec2(0, 1)
		#self.container_elements[1].anchor = vec2(0, 0.333)
		#self.container_elements[2].anchor = vec2(0, -0.333)
		#self.container_elements[3].anchor = vec2(0, -1)



def convert_pygame_screen_pos_to_moderngl_screen_pos(game, position: vec2) -> vec2:
	# Precisely as the function says!
	position = vec2(position)

	# Normalise to 0-1 range.
	position.x /= game.settings.window_resolution.x
	position.y /= game.settings.window_resolution.y

	# Pygame: (0, 0) is top-left. (1, 1) is bottom-right.
	# ModernGL: (-1, 1) is top-left. (1, -1) is bottom-right.
	position.y = 1 - position.y
	position *= 2
	position -= 1

	return position
