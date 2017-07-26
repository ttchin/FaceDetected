import cv2


cap = cv2.VideoCapture(0)
count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces)> 0:
        cv2.imwrite("./image_filter/frame%d.jpg" % count, frame)     # save frame as JPEG file
        count += 1

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    if count > 100:
        cv2.destroyAllWindows()
        break

cap.release()
