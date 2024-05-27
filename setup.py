import sys
from cx_Freeze import setup, Executable

# Dependências
build_exe_options = {"packages": ["tkinter", "pytube", "threading"], "include_files": ["C:\\Users\HP\\Desktop\\Python tkinter\\Youtube downloader Versões\\Youtube versão 2\\icon\\icon.ico"]}

# Executável
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Youtube-Download Versão2",
    version = "2.0",
    description = "Simples Youtube downlader Para Fazer Downloads",
    options = {"YoutubeV2_exe": build_exe_options},
    executables = [Executable("YoutubeV2.py", base=base, icon="C:\\Users\HP\\Desktop\\Python tkinter\\Youtube downloader Versões\\Youtube versão 2\\icon\\icon.ico")]
)
