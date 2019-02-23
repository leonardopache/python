import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).

exe = Executable("main.py",
                 base = "Win32GUI",
                 targetName="Product.exe")


setup(  name = "Product.exe",
        version = "0.1",
        description = "My GUI application!",
        executables = [exe])

