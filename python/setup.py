import sys
import os

# Add this directory to the python path.
# It appears %run does this while running this script and so
# we ignore the first entry in the list.
_dir = os.path.dirname(__file__)
_dbg = False
#print(sys.path)
if _dir not in sys.path[1:]:
    if _dbg: print(f"Adding {_dir} to sys.path")
    sys.path.insert(0, _dir)
else:
    if _dbg: print(f"{_dir} is on sys.path")

########### Following lines appended during installation ##########

