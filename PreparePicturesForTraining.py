from CapturePictures import capturePicturesByCamera
import sys
import os
from enum import Enum
Classify = Enum("Classify", ('Clark','Ye','Weijiao','Chao'))

if __name__ == '__main__':
    args = sys.argv[:]
    if len(args) == 1:
        capturePicturesByCamera()
        os.system("python ImageFilter.py")
    elif len(args) == 2 and args[1] == "split":
        capturePicturesByCamera()
    elif len(args) == 2 and args[1] == "filter":
        os.system("python ImageFilter.py")
    else:
        print("Invalid arguments, only split and filter supported right now...")
