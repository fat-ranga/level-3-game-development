import os

from source.settings import *
import moderngl as mgl
import pygame as pg
import sys
from source.shader_program import ShaderProgram
from source.scene import Scene
from source.player import Player
from source.textures import Textures
from source.user_interface import *


class Main:
	def __init__(self):
		pg.init()
		pg.display.set_caption("Kiwicraft")

		icon = pg.image.load("data/icon.png")
		pg.display.set_icon(icon)

		# Bunch of OpenGL boilerplate stuff.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
		# Prohibit use of deprecated functions.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, Z_DEPTH_SIZE)
		# 24-bit depth for the depth buffer.
		pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)
		
		# Set window resolution from settings and set OpenGl context.
		pg.display.set_mode(WINDOW_RESOLUTION, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
		self.ctx = mgl.create_context()
		
		# Enable fragment depth-testing, culling of invisible faces and colour blending.
		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
		# Automatic garbage collection for OpenGL objects.
		self.ctx.gc_mode = "auto"
		
		self.clock = pg.time.Clock()
		self.delta_time = 0 # Time between frames.
		self.time = 0

		# Makes the current window active, I believe!
		pg.event.set_grab(True)

		# Hides the mouse.
		pg.mouse.set_visible(False)
		
		self.is_running = True
		self.on_init()
	
	def on_init(self):
		self.textures = Textures(self)
		self.player = Player(self)
		self.shader_program = ShaderProgram(self)
		self.scene = Scene(self, texture_ids=self.textures.atlas_packer.texture_ids)
		self.cool_button_au = Button()

		# TODO: better way to pass this data?
		#self.scene.world.texture_ids = self.textures.atlas_packer.texture_ids
		#print("from main" + str(self.textures.atlas_packer.texture_ids))
	
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
			if event.type == pg.QUIT:
				self.is_running = False
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				pg.event.set_grab(False)
				pg.mouse.set_visible(True)

			self.player.handle_event(event=event)
	
	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.render()
		pg.quit()
		sys.exit()


# Magical Python thing!
if __name__ == "__main__":
	# Temporary hack to make working directory the base directory of the project.
	#os.chdir("../")
	game = Main()
	game.run()
