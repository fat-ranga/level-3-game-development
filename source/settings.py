from numba import njit
import numpy as np
import glm
import math
import pygame as pg

# OpenGL settings.
MAJOR_VER, MINOR_VER = 3, 3
Z_DEPTH_SIZE = 24

# Determines whether to cache the result of the LLVM code generated by Numba.
# If there's a random bug that we can't solve, try setting the cache to False.
# When the game is exported, we always want this to be set to True, so end-users
# don't have to wait as long.
LLVM_CACHE_MODE: bool = True

# Antialiasing. Can cause line artifacts in-between triangles
# that have edges that share the same position.
NUM_SAMPLES = 0

# TODO World generation seed.
SEED = 16

# ray casting
MAX_RAY_DIST = 5

# chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# World.
WORLD_W, WORLD_H = 2, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# World centre.
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# Camera stuff.
FOV_DEG = 90
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(90)

# Player.
PLAYER_SPEED = 0.01
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)

# Background world colour.
BG_COLOUR = glm.vec3(0.58, 0.83, 0.99)

# Texture atlas packer.
ATLAS_TEXTURE_ELEMENT_SIZE = 16

# Directories.
DIR_TEXTURES: str = "data/textures/atlas"

# textures
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# terrain levels
SNOW_LVL = 54
STONE_LVL = 49
DIRT_LVL = 40
GRASS_LVL = 8
SAND_LVL = 7

# tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# water
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W

# cloud
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2


# This class contains settings that can be changed by the user, and these
# are saved between sessions using the config file.
class SettingsProfile:
	def __init__(self):
		# Input map.
		self.input_map: dict = {
			"place_voxel": 3,  # Left-click.
			"break_voxel": 1,  # Right-click.
		}
		# Resolution.
		self.window_resolution: glm.vec2 = glm.vec2(720, 720)
		self.mouse_sensitivity: float = 0.002
		# Camera stuff.
		self.aspect_ratio: float = self.window_resolution.x / self.window_resolution.y
		self.fov_deg: int = 90
		self.v_fov: float = glm.radians(FOV_DEG)  # Vertical Field of View.
		self.h_fov: float = 2 * math.atan(math.tan(self.v_fov * 0.5) * self.aspect_ratio)  # Horizontal Field of View.
		self.v_sync: int = 1  # 0 is False.
