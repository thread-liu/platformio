import os
import sys

parameters = " ".join(str(d) for d in sys.argv[1:])
exe_relative_path = 'platformio_core/python.exe'

# determine if application is a script file or frozen exe
dir_path = ""
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(sys.executable)
elif __file__:
    dir_path = os.path.dirname(__file__)

python_path = os.path.join(dir_path, exe_relative_path)
os.system(str(python_path) + " -m platformio " + parameters)
