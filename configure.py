import sys

if 'pytest' in sys.modules:
    DB_NAME = 'temp.db'
else:
    DB_NAME = 'gui.db'
