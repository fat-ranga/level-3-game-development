from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
'packages': ["glcontext"],
'excludes': [],
'include_files' : ["data", "meshes", "shaders", "world_objects"]}
#'include_files' : []

#include_files = ['assets']

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name='test',
      version = '1.0',
      description = 'the',
      options = {'build_exe': build_options},
      executables = executables)
