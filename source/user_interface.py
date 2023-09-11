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
		self.offset: vec2 = vec2(0.0, 0.0)  # Position offset relative to parent position, if any.
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
			local_anchor = self.anchor * self.parent.size
			
			# Scale first...
			offset_from_edges = self.anchor * self.size
			self.position = local_anchor - offset_from_edges
			
			# Then translate.
			self.position += self.parent.position
		
		else:
			offset_from_edges = self.anchor * self.size
			self.position = self.anchor - offset_from_edges
		
		# Correct position for aspect ratio when using offsets.
		aspect_ratio_in_terms_of_x: float = self.game.settings.window_resolution.x / self.game.settings.window_resolution.y
		window_scale_x: float = INITIAL_WINDOW_RESOLUTION.x / self.game.settings.window_resolution.x
		
		aspect_ratio_in_terms_of_y: float = self.game.settings.window_resolution.y / self.game.settings.window_resolution.x
		window_scale_y: float = INITIAL_WINDOW_RESOLUTION.y / self.game.settings.window_resolution.y
		
		self.position.x += self.offset.x * aspect_ratio_in_terms_of_y * window_scale_y
		self.position.y += self.offset.y * aspect_ratio_in_terms_of_x * window_scale_x
	
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


def resize_ui_elements(ui_elements: list):
	for i in range(len(ui_elements)):
		ui_elements[-i - 1].resize()


def update_ui_elements(game, ui_elements: list):
	# Check mouse position and stuff for button selection.
	mouse_pos = pg.mouse.get_pos()
	mouse_pos = convert_pygame_screen_pos_to_moderngl_screen_pos(game, vec2(mouse_pos))
	
	# De-select everything first.
	for i in range(len(ui_elements)):
		ui_elements[i].is_mouse_position_in_bounds = False
	
	# If the mouse isn't visible, then don't try to select anything.
	if not game.mouse_visible:
		return
	
	# Find the first top-most element that the mouse fits in
	# and make that the selected one, ignoring everything underneath.
	for i in range(len(ui_elements)):
		# Move onto the next element if this one doesn't detect the mouse position.
		if not ui_elements[-i - 1].detects_mouse:
			continue
		# If we have something on top selected, make sure not to
		# select anything underneath by returning out of this loop.
		if ui_elements[-i - 1].check_if_mouse_in_bounds(mouse_pos):
			ui_elements[-i - 1].is_mouse_position_in_bounds = True
			return
