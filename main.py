from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures

class Main:
	def __init__(self):
		pg.init()
		pg.display.set_caption("No cap")
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) # Prohibit use of deprecated functions.
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24) # 24-bit depth for the depth buffer.

		# Set window resolution from settings and set OpenGl context.
		pg.display.set_mode(WINDOW_RESOLUTION, flags=pg.OPENGL | pg.DOUBLEBUF)
		self.ctx = mgl.create_context()

		# Enable fragment depth-testing, culling of invisible faces and colour blending.
		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
		self.ctx.gc_mode = "auto" # Automatic garbage collection for OpenGL objects.

		self.clock = pg.time.Clock()
		self.delta_time = 0
		self.time = 0

		pg.event.set_grab(True)
		pg.mouse.set_visible(False)

		self.is_running = True
		self.on_init()

	def on_init(self):
		self.textures = Textures(self)
		self.player = Player(self)
		self.shader_program = ShaderProgram(self)
		self.scene = Scene(self)


	def update(self):
		self.player.update()
		self.shader_program.update()
		self.scene.update()

		self.delta_time = self.clock.tick()
		self.time = pg.time.get_ticks() * 0.001
		pg.display.set_caption(f"{self.clock.get_fps() :.0f}")

	def render(self):
		self.ctx.clear(color=BG_COLOUR) # Clear frame and depth buffers.
		self.scene.render()
		pg.display.flip() # Display a new frame.

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				self.is_running = False

			if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
				pg.event.set_grab(False)
				pg.mouse.set_visible(True)

	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.render()
		pg.quit()
		sys.exit()

# Magical Python thing!
if __name__ == "__main__":
	game = Main()
	game.run()
