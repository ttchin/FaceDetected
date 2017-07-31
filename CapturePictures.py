#!/usr/bin/env python

import cv2
import sys
import argparse

def capturePicturesByCamera(num = 300, saveDir = "./image_filter/"):

    """
    Capture pictures with faces detected.

    Args:
        num (int): The number of pictures to capture. Default: 300.
        saveDir (str): The directory to save the captured pictures. Default: "./image_filter/". Note: Please make sure the directory has been created.

    Returns:
        void

    Todo:
        * Handling of file path construction.
        * Disable logging of cv2.
    """

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
    count = 1

    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the captured frame
        cv2.imshow('Camera', frame)

        # Detect faces in the gray frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        # The frame will be saved when the faces are detected
        if len(faces) > 0:
            # Save frame as JPEG file
            frame_file_path = saveDir + ("frame%d.jpg" % count)
            cv2.imwrite(frame_file_path, frame)
            print("%d picture(s) captured & saved!" % count)
            count += 1

        # Draw rectangles which point out the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Wait for 'q' on the Camera window to quit before entire capturing job finished
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if count > num:
            cv2.destroyAllWindows()
            break

    cap.release()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Capture pictures with faces detected.')
    parser.add_argument('-n', type=int, help='the number of pictures to capture. Default: 300')
    parser.add_argument('-d', type=str, help='the directory to save the captured pictures. Default: "./image_filter/". Note: Please make sure the directory has been created')
    parser.set_defaults(n = 300, d = "./image_filter/")
    args = parser.parse_args()

    # Start the capturing
    capturePicturesByCamera(args.n, args.d)
