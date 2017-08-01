#!/usr/bin/env python

import time
import argparse
from FaceTrain import Model
from FaceInput import getClassifyList
import cv2

face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
model = Model()
model.load()

def detect_faces_from_frame(frame):
    playMusic() #play funny music at the backend
    # Detect faces in the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    #faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
    
    # Match the detected faces with the trained model
    if len(faces) > 0:
        print(">>> Someone is out there!")
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            result = model.predict(face)
            for index, name in getClassifyList():
                if result == index:
                    print(">>> Aha, it's %s!" % name)
                    #return name


def detect_faces_from_picture(pic_file_path):
    print(">>> Let me take a look at this picture: " + pic_file_path)
    frame = cv2.imread(pic_file_path)
    detect_faces_from_frame(frame)


def detect_faces_from_camera_video_stream(exec_time=60):
    # Perform the capture every n seconds
    capture_interval = 0.6

    cap = cv2.VideoCapture(0)
    time_start = time.time()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        detect_faces_from_frame(frame)

        time.sleep(capture_interval)

        if (time.time() - time_start > exec_time):
            break

    cv2.destroyAllWindows()
    cap.release()

def playMusic():
    # pygame.init()
    pygame.mixer.init()
    # screen = pygame.display.set_mode([640, 480])
    pygame.time.delay(2000)
    pygame.mixer.music.load("./dialog/tangbohu.mp3")
    pygame.mixer.music.play()

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Detect faces from the camera video stream or given picutre')
    parser.add_argument('-p', type=str, help='the path of picture to detect faces')
    parser.add_argument('-t', type=int, help='the execution time to detect faces from the camera video stream. Default: 60 seconds')
    parser.set_defaults(t=60)
    args = parser.parse_args()

    # Start detecting
    if args.p == None:
        detect_faces_from_camera_video_stream(args.t)
    else:
        detect_faces_from_picture(args.p)