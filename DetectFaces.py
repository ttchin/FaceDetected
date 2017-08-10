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
sayHello=["Do you remember me", "You are super star", "You looks great today", "I like your eyes", "God bless you", "Do you have free style", "You are so handsome", "You jump I jump", "kiss me baby", "We are Ericsson"]

def detect_faces_from_picture(pic_file_path):
    print(">>> Let me check this picture: " + pic_file_path)
    frame = cv2.imread(pic_file_path)

    # Detect faces in the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
    
    # Match the detected faces with the trained model
    if len(faces) > 0:
        print(">>> Someone is in the picture!")
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            result = model.predict(face)
            for index, name in model.getTrainCfg():
                if result == index:
                    print(">>> Aha, it's %s!" % name)

def detect_faces_from_camera_video_stream(exec_time=60, isAlarm=True):
    # Perform the detection every n seconds
    detect_interval = 2

    cap = cv2.VideoCapture(0)
    exec_start = time.time()
    interval_start = time.time()

    # For calculation of FPS (frame per second)
    frame_num = 0

    detected_name = "World"
    bossName = "Clark"
    alert_interval = 10
    alert_start = 0
    hello_text = ''

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
            if len(faces) > 0:
                print(">>> Someone is out there!")

                x, y, w, h = faces[0]

                face = frame[y:y+h, x:x+w]

                # Draw rectangles which point out the faces
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                label,probe = model.predict(face)
                i = random.randint(0,len(sayHello)-1)
                
                if probe > 0.95:
                    for index, name in model.getTrainCfg():
                        if label == index:
                            detected_name = name
                            
                            if detected_name == bossName and time.time() - alert_start > alert_interval:
                                    alert_start = time.time()
                                    if isAlarm:
                                        playAlert()
                                    
                            print(">>> Aha, it's %s!" % name)
                            
                            if not detected_name == bossName:
                                hello_text = "{}, {}".format(name, sayHello[i])
                                print(hello_text)
                                if isAlarm:
                                    subprocess.Popen(["flite", "-t", hello_text])
                            else:
                                hello_text = "WARING: Boss coming!!!"
                            
                            break
                else:
                    array=["Hello","How are you","Good luck", "Hahaha", "Good afternoon", "Hey hey", "Lu lu lu", "Sa wa di ka", "Ah yi xi", "Ka wa yi","kou ni qi wa"]
                    i = random.randint(0,len(array)-1)
                    
                    hello_text = array[i]
                    print(hello_text)
                    
                    if isAlarm:
                        subprocess.Popen(["flite","-t", hello_text])
                
        # Display the camero video
        cv2.putText(frame, "Press 'q' to quit", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, hello_text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
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
    pygame.mixer.music.load(array[(alert_track%3) - 1])
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    print("volume %f" % pygame.mixer.music.get_volume())
    alert_track += 1

def otherFace():
    array=["Hello","How are you","Good luck", "Hahaha", "Good afternoon", "Hey hey", "Lu lu lu", "Sa wa di ka", "Ah yi xi", "Ka wa yi","kou ni qi wa"]
    randomValue = random.randint(0,len(array)-1)
    
    hello_text = "{}, {}".format(name, sayHello[i])
    print(hello_text)
    
    if isAlarm:
        subprocess.Popen(["flite","-t", "{}".format(array[randomValue])])

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Detect faces from the camera video stream or given picutre')
    parser.add_argument('-p', type=str, help='the path of picture to detect faces')
    parser.add_argument('-t', type=int, help='the execution time to detect faces from the camera video stream. Default: 60 seconds')
    parser.set_defaults(t=60)
    parser.add_argument('--alarm', dest='alarm', default=False, help='Alarm when detecting the boss')
    
    args = parser.parse_args()
    print(args.alarm)
    # Start detecting
    if args.p == None:
        detect_faces_from_camera_video_stream(args.t,args.alarm)
    else:
        detect_faces_from_picture(args.p)
