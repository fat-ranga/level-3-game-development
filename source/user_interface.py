from source.settings import *
import pygame as pg
from glm import vec2, ivec2
from source.meshes.ui_quad_mesh import QuadMesh


class Control:
	def __init__(self, game):
		self.game = game

		self.visible: bool = True
		self.keep_aspect: bool = True
		self.name = "default"
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

		#if self.parent:
		#	self.position.x = self.anchor.x - 0#(self.size.x / 1)
		#	self.position.y = self.anchor.y - (self.size.y / 1)

		if self.parent:
			print("has parent")
			offset_from_edges = self.anchor * self.size
			self.position = self.anchor - offset_from_edges
			print(self.position)
			self.position += self.parent.position
			print(self.position)
		else:
			offset_from_edges = self.anchor * self.size
			self.position = self.anchor - offset_from_edges

		#if self.parent:
			#self.position = self.parent.position + self.anchor

	# self.size = self.scale
	# self.size.x *= aspect_ratio_correction

	# self.position = self.size

	def update(self):
		if not self.visible:
			return

		# if not self.parent:
		#	self.position = vec2(self.game.settings.window_resolution.x, self.game.settings.window_resolution.y) * self.anchor
		# else:
		#	self.position = self.parent.position * self.anchor

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


class Button(TextureRect):
	def __init__(self, game):
		super().__init__(game)
		self.game = game
		self.is_selected: bool = False
		self.is_selected_texture_id: int = self.texture_id

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


class Container(Control):
	def __init__(self):
		super().__init__()


class VBoxContainer(Container):
	def __init__(self):
		super().__init__()


def convert_pg_screen_pos_to_moderngl_screen_pos(game, position: vec2) -> vec2:
	# Precisely as the function says!
	position = vec2(position)

	# Normalise to 0-1 range.
	position.x /= game.settings.window_resolution.x
	position.y /= game.settings.window_resolution.y

	# Pygame: (0, 0) is top-left. (1, 1) is bottom-right.
	# ModernGL: (-1, 1) is top-left. (1, -1) is bottom-right.
	position.y = 1 - position.y
	position *= 2
	position.x -= 1
	position.y -= 1

	return position
