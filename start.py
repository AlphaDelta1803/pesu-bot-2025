import sys #provides access to variables and functions that can be used to manipulate different parts of the python run time environment
import subprocess #the subprocess module lets you spawn new processes, connect to their input/output/error pipes, and obtain their return codes
p = subprocess.Popen(['/bin/bash', '-i', '-c', 'botstart'])
sys.exit(0)
