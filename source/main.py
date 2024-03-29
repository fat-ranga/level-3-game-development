import os
import sys
import pygame as pg
import moderngl as mgl

import source.settings
from source.settings import *
from source.shader_program import ShaderProgram
from source.scene import Scene
from source.player import Player
from source.camera import Camera
from source.textures import Textures
from source.user_interface import *
from source.data_definitions import *
from source.main_menu import MainMenu


class Main:
	def __init__(self):
		pg.init()

		pg.display.set_caption("Compiling...")  # Window name.

		icon = pg.image.load("data/icon.png")  # Window icon.
		pg.display.set_icon(icon)

		# Load settings from configuration file next to executable.
		self.settings: SettingsProfile = self.load_settings()

		# Bunch of OpenGL boilerplate stuff.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
		# Prohibit use of deprecated functions, since we are using version 3.3, which is 'modern' OpenGL.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, Z_DEPTH_SIZE)
		# 24-bit depth for the depth buffer.
		pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)

		# Set window resolution from settings.
		pg.display.set_mode(self.settings.window_resolution, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE,
							vsync=self.settings.v_sync)

		# Grabs the window context created by pygame.
		# This is what we send all our vertex data and rendering stuff to.
		self.ctx = mgl.create_context()

		# Enable fragment depth-testing, culling of invisible faces and alpha blending.
		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
		# Automatic garbage collection for OpenGL objects.
		self.ctx.gc_mode = "auto"

		self.clock = pg.time.Clock()
		self.delta_time = 0  # Time between frames.
		self.time = 0
		self.paused = False
		self.is_game_started = False

		self.grab_mode: bool = False
		self.mouse_visible: bool = True
		pg.event.set_grab(self.grab_mode)  # Constrains the mouse to window bounds.
		pg.mouse.set_visible(self.mouse_visible)  # Shows or hides the mouse.

		self.is_running = True  # If we set this to False, the program closes.

		self.on_init()

	def load_settings(self) -> SettingsProfile:
		# TODO: read from config file

		return SettingsProfile()

	def on_init(self):
		# pg.display.set_caption("Kiwicraft")
		self.paused = True

		pg.display.set_caption("Loading textures...")
		self.textures = Textures(self)
		pg.display.set_caption("Loading voxel data...")
		self.voxel_data: VoxelDataDictionary = load_voxel_data(
			"data/voxel_types.json",
			self.textures.atlas_packer.texture_ids)
		# todo temp
		pg.display.set_caption("Making camera...")
		self.menu_camera = Camera(glm.vec3(0, 0, 0),
								  0,
								  0,
								  self.settings.v_fov,
								  self.settings.h_fov,
								  self.settings.aspect_ratio)

		pg.display.set_caption("Creating shader program...")
		self.shader_program = ShaderProgram(self, self.menu_camera)

		pg.display.set_caption("Creating main menu...")
		self.main_menu = MainMenu(self)
		pg.display.set_caption("Kiwicraft")

	def start_game(self):
		self.paused = False
		self.is_game_started = True

		# Hides the mouse.
		self.mouse_visible = False
		pg.mouse.set_visible(self.mouse_visible)
		# Constrains the mouse to the window.
		self.grab_mode = True
		pg.event.set_grab(self.grab_mode)

		self.player = Player(self, self.voxel_data)
		self.shader_program.current_camera = self.player
		self.shader_program.update_projection_matrix()
		self.scene = Scene(self,
						   texture_ids=self.textures.atlas_packer.texture_ids,
						   voxel_data=self.voxel_data)

		# Starting the mixer.
		#pg.mixer.init()
		# Loading the song.
		#pg.mixer.music.load("data/audio/46-tui-morning-chorus.mp3")
		# Setting the volume.
		#pg.mixer.music.set_volume(0.7)
		# Start playing the song.
		#pg.mixer.music.play()

	def update(self):
		# todo: change this to a reference variable like 'current_scene' or something maybe
		if not self.paused:
			self.player.update()
			self.shader_program.update()
			self.scene.update()
		else:
			self.main_menu.update()

		self.delta_time = self.clock.tick()
		self.time = pg.time.get_ticks() * 0.001

		pg.display.set_caption(f"{self.clock.get_fps() :.0f}")

	def render(self):
		self.ctx.clear(color=BG_COLOUR)  # Clear frame and depth buffers.
		if self.is_game_started:
			self.scene.render()
		else:
			self.main_menu.render()
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
				pg.display.toggle_fullscreen()

			if event.type == pg.VIDEORESIZE:
				# Recalculate aspect ratio and stuff.
				self.settings.window_resolution = vec2(event.size[0], event.size[1])
				self.settings.aspect_ratio = self.settings.window_resolution.x / self.settings.window_resolution.y
				self.settings.h_fov = 2 * math.atan(math.tan(self.settings.v_fov * 0.5) * self.settings.aspect_ratio)

				if self.is_game_started:
					# Update projection matrix so that the view doesn't become squashed or stretched.
					self.player.update_projection_matrix()
					self.shader_program.update_projection_matrix()

					# Correct aspect ratio of UI elements.
					self.scene.rebuild_ui()
				else:
					self.main_menu.rebuild_ui()
			if self.is_game_started:
				self.player.handle_event(event=event)
			else:
				self.main_menu.handle_event(event=event)

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
