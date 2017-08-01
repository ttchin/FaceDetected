#! encoding: UTF-8
import cv2
import sys
import pygame
from FaceTrain import Model
from FaceInput import getClassifyList


def detectFace(picturePath):
    playMusic() #play funny music at the backend
    frame = cv2.imread(picturePath)
    cascade_path = "opencv_config/haarcascade_frontalface_default.xml"
    model = Model()
    model.load()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

    while 1:
        #for event in pygame.event.get():
         #   if event.type == pygame.QUIT:
          #      pygame.mixer.music.stop()
        if not pygame.mixer.music.get_busy():
            break
            
    if len(facerect) > 0:
        print('face detected')
        for rect in facerect:
            x, y = rect[0:2]
            width, height = rect[2:4]
            # why y -10?
            image = frame[y - 10: y + height, x: x + width]
            result = model.predict(image)
            for i, item in getClassifyList():
                if result == i:
                    print("%s is appoaching" % item)
                    return item

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

def playMusic():
    # pygame.init()
    pygame.mixer.init()
    # screen = pygame.display.set_mode([640, 480])
    pygame.time.delay(2000)
    pygame.mixer.music.load("./dialog/tangbohu.mp3")
    pygame.mixer.music.play()

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

