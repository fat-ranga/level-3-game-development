import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6"],
    "includes": ["glcontext"],
    "include_files": ["data"],
    "optimize": 1,
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Kiwicraft",
    version="0.1",
    description="Level 3 Game Development Project",
    options={"build_exe": build_exe_options},
    executables=[Executable("source/main.py", base=base, target_name="Kiwicraft")],
)
