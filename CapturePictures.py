#!/usr/bin/env python

"""
Python script to capture pictures with faces detected.
"""

import os
import argparse
import cv2

def capture_pictures_by_camera(num=200, save_dir="./captured_pictures"):

    """
    Capture pictures with faces detected and the cropped face images will be saved under "cropped_faces" folder.

    Args:
        num (int): The number of pictures to capture. Default: 200
        save_dir (str): The directory to save the captured pictures. Default: "./captured_pictures/"

    Returns:
        void

    Todo:
        * Disable logging of cv2.
    """

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
    jpg_file_ext = ".jpg"
    frame_index = 1

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
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

            frame_file_name = "frame%d" % frame_index
            frame_file_name_with_ext = frame_file_name + jpg_file_ext
            frame_file_path = os.path.join(save_dir, frame_file_name_with_ext)
            cv2.imwrite(frame_file_path, frame)

            print("%d picture(s) captured & saved!" % frame_index)
            frame_index += 1

            for (x, y, w, h) in faces:
                face_index = 1

                # Draw rectangles which point out the faces
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                face_file_dir = os.path.join(save_dir, "cropped_faces")
                if not os.path.exists(face_file_dir):
                    os.mkdir(face_file_dir)

                face_file_name_with_ext = frame_file_name + ("-face%d" % face_index) + jpg_file_ext
                face_file_path = os.path.join(face_file_dir, face_file_name_with_ext)

                # Save cropped face as JPEG file
                face = frame[y:y+h, x:x+w]
                cv2.imwrite(face_file_path, face)

        # Wait for 'q' on the Camera window to quit before entire capturing job finished
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if frame_index > num:
            cv2.destroyAllWindows()
            break

    cap.release()

    print("==============================================================================")
    print("Now you could get the captured pictures under directory: " + save_dir)
    print("==============================================================================")


if __name__ == '__main__':

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Capture pictures with faces detected.')
    parser.add_argument('-n', type=int, help='the number of pictures to capture. Default: 200')
    parser.add_argument('-d', type=str, help='the directory to save the captured pictures. Default: "./captured_pictures"')
    parser.set_defaults(n = 200, d = "./captured_pictures")
    args = parser.parse_args()

    # Start the capturing
    capture_pictures_by_camera(args.n, args.d)
