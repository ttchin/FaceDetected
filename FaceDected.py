#! encoding: UTF-8
import cv2
import sys
from FaceTrain import Model
import os
import time


def detectFace(picturePath):
    frame = cv2.imread(picturePath)
    cascade_path = "opencv_config/haarcascade_frontalface_default.xml"
    model = Model()
    model.load()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

    if len(facerect) > 0:
        print('face detected')
        for rect in facerect:
            x, y = rect[0:2]
            width, height = rect[2:4]
            image = frame[y - 10: y + height, x: x + width]
            result = model.predict(image)
            if result == 0:  # boss
                print('Clark is approaching')
                return "Clark"
            elif result == 1:
                print('Ye is approaching')
                return "Ye"
            elif result == 2:
                print('Weijiao is approaching')
                return "Weijiao"
            else:
                print('Chao is approaching')
                return "Chao"

def capturePicture():
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            cv2.imwrite("tmpFaceImage.jpg", frame)  # save frame as JPEG file
            cv2.destroyAllWindows()
            break
    cap.release()

    return "tmpFaceImage.jpg"


if __name__ == '__main__':
    args = sys.argv[:]
    #print (args)
    if (len(args) ==1):
        results = detectFace(capturePicture())
    elif (len(args) == 2):
        results = detectFace(sys.argv[1])
    else:
        print("Please input the path of the face picture, only 1 picture at a time")
        quit()
