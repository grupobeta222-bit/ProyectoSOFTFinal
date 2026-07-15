import os
import subprocess
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
os.chdir(CARPETA)
subprocess.run([sys.executable, "src/interfaces/presentation/app_ui.py"])
