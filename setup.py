import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "plyer", "tkinter"],
    "include_files": [],
}

setup(
    name="Guardian",
    version="5.1",
    description="Sistema de Bienestar Digital",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", target_name="Guardian.exe")],
)
