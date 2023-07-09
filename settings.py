from numba import njit
import numpy as np
import glm
import math as maths

# Initial window resolution.
WINDOW_RESOLUTION = glm.vec2(854, 480)

# Colours.
BG_COLOUR = glm.vec3(0.1, 0.16, 0.25)