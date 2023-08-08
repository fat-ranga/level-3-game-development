import os

import source.settings
from source.settings import *
import moderngl as mgl
import pygame as pg
import sys
from source.shader_program import ShaderProgram
from source.scene import Scene
from source.player import Player
from source.textures import Textures
from source.user_interface import *
from source.data_definitions import *


class Main:
	def __init__(self):
		pg.init()
		pg.display.set_caption("Kiwicraft")

		icon = pg.image.load("data/icon.png")
		pg.display.set_icon(icon)

		# Load settings from configuration file next to executable.
		self.settings: SettingsProfile = self.load_settings()

		# Bunch of OpenGL boilerplate stuff.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
		# Prohibit use of deprecated functions.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, Z_DEPTH_SIZE)
		# 24-bit depth for the depth buffer.
		pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)

		# Set window resolution from settings and set OpenGl context.
		pg.display.set_mode(self.settings.window_resolution, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE,
							vsync=self.settings.v_sync)
		self.ctx = mgl.create_context()

		# Enable fragment depth-testing, culling of invisible faces and colour blending.
		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
		# Automatic garbage collection for OpenGL objects.
		self.ctx.gc_mode = "auto"

		self.clock = pg.time.Clock()
		self.delta_time = 0  # Time between frames.
		self.time = 0

		self.grab_mode: bool = True
		self.mouse_visible: bool = False

		# Makes the current window active, I believe!
		pg.event.set_grab(self.grab_mode)

		# Hides the mouse.
		pg.mouse.set_visible(self.mouse_visible)

		self.is_running = True
		self.on_init()

	def load_settings(self) -> SettingsProfile:
		# TODO: read from config file

		return SettingsProfile()

	def on_init(self):
		self.textures = Textures(self)
		self.voxel_data: VoxelDataDictionary = load_voxel_data(self,
															   "data/voxel_types.json",
															   self.textures.atlas_packer.texture_ids)
		self.player = Player(self, self.voxel_data)
		self.shader_program = ShaderProgram(self)
		self.scene = Scene(self,
						   texture_ids=self.textures.atlas_packer.texture_ids,
						   voxel_data=self.voxel_data)

	def update(self):
		self.player.update()
		self.shader_program.update()
		self.scene.update()

		self.delta_time = self.clock.tick()
		self.time = pg.time.get_ticks() * 0.001
		pg.display.set_caption(f"{self.clock.get_fps() :.0f}")

	def render(self):
		self.ctx.clear(color=BG_COLOUR)  # Clear frame and depth buffers.
		self.scene.render()
		pg.display.flip()  # Display a new frame.

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.is_running = False

			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				self.grab_mode = not self.grab_mode
				self.mouse_visible = not self.mouse_visible

				pg.event.set_grab(self.grab_mode)
				pg.mouse.set_visible(self.mouse_visible)

			if event.type == pg.KEYDOWN and event.key == pg.K_F11:
				# pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
				pg.display.toggle_fullscreen()

			if event.type == pg.VIDEORESIZE:
				# Update aspect ratio and stuff when the window is resized.
				self.settings.window_resolution = vec2(event.size[0], event.size[1])
				self.settings.aspect_ratio = self.settings.window_resolution.x / self.settings.window_resolution.y
				self.settings.h_fov = 2 * math.atan(math.tan(self.settings.v_fov * 0.5) * self.settings.aspect_ratio)

				self.scene.crosshair.mesh.rebuild()
				self.player.update_projection_matrix()
				self.shader_program.update_projection_matrix()

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
	# os.chdir("../")
	game = Main()
	game.run()
