from settings import *
from world_objects.chunk import Chunk


class Scene:
	def __init__(self, game):
		self.game = game
		self.chunk = Chunk(self.game)

	def update(self):
		pass

	def render(self):
		self.chunk.render()