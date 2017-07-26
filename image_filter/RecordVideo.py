#! encoding: UTF-8
import os
import datetime as dt
import picamera
import random

destination = './videos'
camera = picamera.PiCamera()
camera.vflip = True

filename = os.path.join(destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
camera.start_recording(filename)
sleep(60)
camera.stop_recording()