from source.settings import *
import pygame as pg
from glm import vec2
from source.meshes.ui_quad_mesh import QuadMesh


class Control:
	def __init__(self, game):
		self.game = game

		self.visible: bool = True
		self.keep_aspect: bool = True
		self.z_depth: float = 0.0

		# All relative to the Control's bounding box.
		self.origin: vec2 = vec2(0.0, 1.0)  # In OpenGL it is bottom-left, this makes it top-left.
		self.margin: vec2 = vec2(0.0, 0.0)
		self.anchor: vec2 = vec2(0.5, 0.5)
		self.size: vec2 = vec2(0.5, 0.5)

		# Position value is determined from the other values, and is not used directly.
		self.position: vec2 = vec2(0.0, 0.0)  # Local position, relative to parent.
		self.parent: Control = None

	def resize(self):
		pass

		#self.position = self.size

	def update(self):
		if not self.visible:
			return

		if not self.parent:
			self.position = vec2(self.game.settings.window_resolution.x, self.game.settings.window_resolution.y) * self.anchor
		else:
			self.position = self.parent.position * self.anchor

		self.render()

	def render(self):
		pass


class Button(Control):
	def __init__(self, game):
		super().__init__(game)
		#self.texture = None
		self.game = game
		self.mesh = QuadMesh(self)

	def render(self):
		self.mesh.render()


class TextureRect(Control):
	def __init__(self, game):
		super().__init__(game)
		self.game = game
		self.mesh = QuadMesh(self)

	def render(self):
		self.mesh.render()

class Container(Control):
	def __init__(self):
		super().__init__()

class VBoxContainer(Container):
	def __init__(self):
		super().__init__()