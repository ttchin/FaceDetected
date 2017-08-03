#!/usr/bin/env python

import time
import argparse
import pygame
from FaceTrain import Model
import cv2
import subprocess
import random


face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
model = Model()
model.load()
alert_track = 1
sayHello=["Do you remember me", "I am trying to remember your name", "I think you are super star", "You looks great today", "I like your eyes", "God bless you", "Do you have free style"]

def detect_faces_from_picture(pic_file_path):
    print(">>> Let me check this picture: " + pic_file_path)
    frame = cv2.imread(pic_file_path)

    # Detect faces in the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    #faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
    
    # Match the detected faces with the trained model
    if len(faces) > 0:
        print(">>> Someone is in the picture!")
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            result = model.predict(face)
            for index, name in model.getTrainCfg():
                if result == index:
                    print(">>> Aha, it's %s!" % name)

def detect_faces_from_camera_video_stream(exec_time=60):
    # Perform the detection every n seconds
    detect_interval = 2

    cap = cv2.VideoCapture(0)
    exec_start = time.time()
    interval_start = time.time()

    # For calculation of FPS (frame per second)
    frame_num = 0

    detected_name = "World"
    bossName = "Leo"
    alert_interval = 20
    alert_start = 0


    while True:
        if time.time() - exec_start > exec_time:
            break

        # Capture frame-by-frame
        _, frame = cap.read()
        frame_num += 1

        if time.time() - interval_start > detect_interval:
            interval_start = time.time()

            # Detect faces in the frame
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            #faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
            
            # Match the detected faces with the trained model
            if len(faces) == 1:
                print(">>> Someone is out there!")
                otherFace()
                isBoss = False
                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]

                    # Draw rectangles which point out the faces
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    label,probe = model.predict(face)
                    if probe > 0.95:
                        for index, name in model.getTrainCfg():
                            if label == index:
                                if name == detected_name:
                                    isSamePeople = True
                                else:
                                    isSamePeople = False
                                
                                detected_name = name
                                
                                if detected_name == bossName and time.time() - alert_start > alert_interval:
                                        alert_start = time.time()
                                        playAlert()
                                        
                                if not isSamePeople:
                                    print(">>> Aha, it's %s!" % name)
                                    #subprocess.Popen(["espeak", "hello {}, have a nice day".format(name)])
                                    subprocess.Popen(["flite", "-t", "{}".format(name)])
                                else:
                                    i = random.randint(0,len(sayHello)-1)
                                    #subprocess.Popen(["espeak", "{}".format(sayHello[i])])
                                    subprocess.Popen(["flite","-t", "{}".format(sayHello[i])])
                                break
            elif len(faces) > 1:
                print("Too many people here, I am going to die!")
                
        # Display the camero video
        cv2.putText(frame, "Press 'q' to quit", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, ("FPS: %0.2f" % (frame_num / (time.time() - exec_start))),
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, ("Hello, %s!" % detected_name), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Camera', frame)
        
        # Wait for 'q' on the Camera window to quit before entire capturing job finished
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()

def playAlert():
    global alert_track
    print(">>> Boss is comming, Alert!!!")
    print("\n")
    array=["./dialog/boss-ye.wav","./dialog/leo.wav", "./dialog/clark.wav"]
    pygame.mixer.init()
    # pygame.time.delay(2000)
    pygame.mixer.music.load(array[(alert_track%3) - 1])
    pygame.mixer.music.play()
    alert_track += 1

def otherFace():
    array=["Hello","How are you","Good luck", "Hahaha", "Good afternoon", "Hey hey", "Lu lu lu", "Sa wa di ka", "Ah yi xi", "Ka wa yi","kou ni qi wa"]
    randomValue = random.randint(0,len(array)-1)
    #subprocess.Popen(["espeak", "{}".format(array[randomValue])])
    subprocess.Popen(["flite","-t", "{}".format(array[randomValue])])

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
