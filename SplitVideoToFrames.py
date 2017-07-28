import cv2

def slitPictures():
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
            print("%d pictures has been captured" % count)

        for (x, y, w, h) in faces:
            # a,b,c,d = cv2.boundingRect(cnt)
            # cv2.rectangle(image, (a, b), (a + c, b + d), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            cv2.destroyAllWindows()

        # Display the resulting frame
        # cv2.imshow('frame',gray)
        if count > 300:
            cv2.destroyAllWindows()
            break

    cap.release()
