from CapturePictures import capture_pictures_by_camera
import sys
import os
from enum import Enum
Classify = Enum("Classify", ('Clark','Ye','Weijiao','Chao'))

if __name__ == '__main__':
    args = sys.argv[:]
    if len(args) == 1:
        capture_pictures_by_camera()
        os.system("python ImageFilter.py")
    elif len(args) == 2 and args[1] == "split":
        capture_pictures_by_camera()
    elif len(args) == 2 and args[1] == "filter":
        os.system("python ImageFilter.py")
    else:
        print("Invalid arguments, only split and filter supported right now...")
