#! encoding: UTF-8
import cv2
import sys
from FaceTrain import Model


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
                print('Boss is approaching')

            else:
                print('Not boss')


if __name__ == '__main__':
    args = sys.argv[:]
    print (args)
    if (len(args) != 2):
        print("Please input the path of the face picture, only 1 picture at a time")
        quit()

    picturePath = sys.argv[1]
    detectFace(picturePath)
