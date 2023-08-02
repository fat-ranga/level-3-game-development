from source.settings import *
import pygame as pg
from glm import vec2


class Control:
	def __init__(self):
		self.visible: bool = True
		self.margin: vec2 = vec2(0.0, 0.0)
		self.anchor: vec2 = vec2(0.5, 0.5) #
		self.position: vec2 = vec2(0.0, 0.0)  # Local position, relative to parent.
		self.parent: Control = None

	def update(self):
		if not self.visible:
			return

		#self.
		self.render()

	def render(self):
		pass


class Button(Control):
	def __init__(self):
		super().__init__()
		print(self.position.x)
		print(f"margin y is {self.margin.y}")


class TextureRect(Control):
	def __init__(self):
		super().__init__()


class Container(Control):
	def __init__(self):
		super().__init__()
