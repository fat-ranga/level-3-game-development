from numba import njit
import numpy as np
import glm
import math as maths

# Initial window resolution.
WINDOW_RESOLUTION = glm.vec2(854, 480)

# Colours.
BG_COLOUR = glm.vec3(0.1, 0.16, 0.25)

# Chunk.
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE / 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE

# Camera.
ASPECT_RATIO = WINDOW_RESOLUTION.x / WINDOW_RESOLUTION.y
FOV_DEG = 90
V_FOV = glm.radians(FOV_DEG)
H_FOV = maths.atan(maths.tan(V_FOV * 0.5) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000
PITCH_MAX = glm.radians(90)

# Player.
PLAYER_SPEED = 0.01
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(H_CHUNK_SIZE, CHUNK_SIZE, 1.5 * CHUNK_SIZE)
MOUSE_SENSITIVITY = 0.002
