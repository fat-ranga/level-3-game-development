from numba import njit
import numpy as np
import glm
import math

# OpenGL settings.
MAJOR_VER, MINOR_VER = 3, 3
Z_DEPTH_SIZE = 24

# Anti-aliasing, can cause line artifacts in-between triangles
# that have edges that share the same position.
NUM_SAMPLES = 0

# Resolution.
WINDOW_RESOLUTION = glm.vec2(812, 480)

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
WORLD_W, WORLD_H = 10, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# World centre.
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# Camera stuff.
ASPECT_RATIO = WINDOW_RESOLUTION.x / WINDOW_RESOLUTION.y
FOV_DEG = 90
V_FOV = glm.radians(FOV_DEG)  # Vertical Field of View.
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # Horizontal Field of View.
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(90)

# Player.
PLAYER_SPEED = 0.01
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)
#PLAYER_POS = glm.vec3(CENTER_XZ, CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# Background world colour.
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

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
