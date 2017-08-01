import cv2
import sys
import os
import os.path

# cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # img = cv2.imread(frame, 0)
    # ret1, thresh = cv2.threshold(gray, 127, 255, 0)
    # image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cnt = contours[0]

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))
    # ret, thresh = cv2.threshold(img, 127, 255, 0)
    # contours, hierarchy = cv2.findContours(thresh, 1, 2)
    # cnt = contours[0]
    # x, y, w, h = cv2.boundingRect(cnt)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # a,b,c,d = cv2.boundingRect(cnt)
        # cv2.rectangle(image, (a, b), (a + c, b + d), (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()