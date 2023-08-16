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
		self.is_selected = False
		self.is_mouse_position_in_bounds = False

		# All relative to the Control's bounding box.
		self.margin: vec2 = vec2(0.0, 0.0)
		self.anchor: vec2 = vec2(0.5, 0.5) # (0,0) is centre of screen in ModernGL.
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

		#self.size = self.scale
		#self.size.x *= aspect_ratio_correction

		#self.position = self.size

	def update(self):
		if not self.visible:
			return

		#if not self.parent:
		#	self.position = vec2(self.game.settings.window_resolution.x, self.game.settings.window_resolution.y) * self.anchor
		#else:
		#	self.position = self.parent.position * self.anchor

		self.render()

	def check_if_mouse_in_bounds(self, target_position: vec2):
		self.is_mouse_position_in_bounds = False
		if target_position.x < self.position.x - self.size.x:
			return
		if target_position.x > self.position.x + self.size.x:
			return
		if target_position.y < self.position.y - self.size.y:
			return
		if target_position.y > self.position.y + self.size.y:
			return

		self.is_mouse_position_in_bounds = True
		return


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

	def render(self):
		super().render()




class Container(Control):
	def __init__(self):
		super().__init__()

class VBoxContainer(Container):
	def __init__(self):
		super().__init__()