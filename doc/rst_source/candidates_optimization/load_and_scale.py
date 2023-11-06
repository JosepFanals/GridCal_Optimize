from GridCal.Engine import *
from GridCal.Engine.IO.file_handler import FileOpen, FileSave

grid = FileOpen('Spain.gridcal').open()
# The ieee118 .gridcal file may be damaged, redo or pick another grid
print('Done')
