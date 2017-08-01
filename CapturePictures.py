#!/usr/bin/env python

"""
Python script to capture pictures with faces detected.
"""

import os
import time
import argparse
import cv2

def capture_pictures_by_camera(num=200, save_dir="./captured_pictures", no_face_cropping=False, no_capture_saving=False):

    """
    Capture pictures with faces detected and the cropped face images will be saved under "cropped_faces" folder if face cropping function is enabled.

    Args:
        num (int): The number of pictures to capture. Default: 200
        save_dir (str): The directory to save the captured pictures. Default: "./captured_pictures/"
        no_face_cropping (bool): If NOT to do face cropping and save the cropped face images under "cropped_faces" folder. Default: False
        no_capture_saving (bool): If NOT to store the captured pictures to save time. Default: False

    Returns:
        void

    Todo:
        * Disable logging of cv2.
    """

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
    jpg_file_ext = ".jpg"
    captured_frame_index = 0

    # For calculation of FPS (frame per second)
    frame_num = 0
    time_start = time.time()

    # Perform the capture every n frames
    # Enlarge this value will increase the FPS
    capture_every_n_frames = 4

    # Create directory for captured pictures if it's not existing
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # Create directory for cropped face images if it's not existing
    if not no_face_cropping:
        face_file_dir = os.path.join(save_dir, "cropped_faces")
        if not os.path.exists(face_file_dir):
            os.mkdir(face_file_dir)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_num += 1

        # Only perform the capture every n frames
        if frame_num % capture_every_n_frames == 0:
            # Detect faces in the gray frame
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

            # The frame will be saved when the faces are detected
            if len(faces) > 0:
                captured_frame_index += 1
                print("%d picture(s) captured!" % captured_frame_index)

                frame_file_name = "frame%d" % captured_frame_index

                # Save frame as JPEG file
                if not no_capture_saving:
                    frame_file_name_with_ext = frame_file_name + jpg_file_ext
                    frame_file_path = os.path.join(save_dir, frame_file_name_with_ext)
                    cv2.imwrite(frame_file_path, frame)

                face_index = 1
                for (x, y, w, h) in faces:
                    if not no_face_cropping:
                        face_file_name_with_ext = frame_file_name + ("-face%d" % face_index) + jpg_file_ext
                        face_file_path = os.path.join(face_file_dir, face_file_name_with_ext)

                        # Save cropped face as JPEG file
                        face = frame[y:y+h, x:x+w]
                        cv2.imwrite(face_file_path, face)

                    # Draw rectangles which point out the faces
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    face_index += 1

        # Display the captured frame
        cv2.putText(frame, "Press 'q' to quit", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.putText(frame, ("FPS: %0.2f" % (frame_num / (time.time() - time_start))), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.putText(frame, ("%d picture(s) captured!" % captured_frame_index), (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow('Camera', frame)
        
        # Wait for 'q' on the Camera window to quit before entire capturing job finished
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        if captured_frame_index >= num:
            cv2.destroyAllWindows()
            break  

    cap.release()

    print("==============================================================================")
    print("Now you could get the captured pictures under directory: " + save_dir)

    if not no_face_cropping:
        print("And the cropped face images under directory: " + face_file_dir)

    print("==============================================================================")


if __name__ == '__main__':

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Capture pictures with faces detected.')
    parser.add_argument('-n', type=int, help='the number of pictures to capture. Default: 200')
    parser.add_argument('-d', type=str, help='the directory to save the captured pictures. Default: "./captured_pictures"')
    parser.add_argument('--no-face-cropping', action='store_const', default = 'False', const = 'True', dest='no_face_cropping', help='not to do the face cropping. Default: False')

    parser.add_argument('--no-capture-saving', action='store_const', default = 'False', const = 'True', dest='no_capture_saving', help='not to store the captured pictures to save time. Default: False')

    parser.set_defaults(n=200, d="./captured_pictures", no_face_cropping=False, no_capture_saving=False)

    args = parser.parse_args()

    # Start capturing
    capture_pictures_by_camera(args.n, args.d, args.no_face_cropping, args.no_capture_saving)
