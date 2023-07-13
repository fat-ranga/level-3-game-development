from source.settings import SEED
from numba import njit
from opensimplex.internals import _noise2, _noise3, _init

# TODO: Set the seed for all our noise values to the world seed.
perm, perm_grad_index3 = _init(seed=SEED)


@njit(cache=True) # Real true
def noise2(x, y):
	return _noise2(x, y, perm)


@njit(cache=True) # Real true
def noise3(x, y, z):
	return _noise3(x, y, z, perm, perm_grad_index3)
