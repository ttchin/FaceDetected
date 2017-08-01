#!/usr/bin/env python
"""
Python script to crop faces from pictures under the specified directory.
"""

import os
import argparse
import cv2


def crop_faces_from_pictures(pic_dir):
    """
    Crop faces from pictures under the specified directory and the cropped face images will be saved under "cropped_faces" folder.

    Args:
        pic_dir (str): The directory of pictures to do face cropping

    Returns:
        void

    Todo:
        * 
    """

    jpg_file_ext = ".jpg"

    face_file_dir = os.path.join(pic_dir, "cropped_faces")
    if not os.path.exists(face_file_dir):
        os.mkdir(face_file_dir)

    face_cascade = cv2.CascadeClassifier(
        'opencv_config/haarcascade_frontalface_default.xml')

    pic_files = os.listdir(pic_dir)
    for pic_file in pic_files:
        # Only handle JPEG image files
        if pic_file.endswith(jpg_file_ext):
            pic = cv2.imread(os.path.join(pic_dir, pic_file))
            gray_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_pic, 1.3, 5)

            if len(faces) > 0:
                print('%d face(s) detected in %s' % (len(faces), pic_file))

                # Save cropped face as JPEG file
                face_index = 1
                for (x, y, w, h) in faces:
                    face = pic[y:y + h, x:x + w]
                    face_file_name_with_ext = pic_file.replace(
                        jpg_file_ext,
                        '') + ("-face%d" % face_index) + jpg_file_ext
                    face_file_path = os.path.join(face_file_dir,
                                                  face_file_name_with_ext)
                    cv2.imwrite(face_file_path, face)
                    face_index += 1

    print(
        "=============================================================================="
    )
    print("Now you could get the cropped face images under directory: " +
          face_file_dir)
    print(
        "=============================================================================="
    )


def main():
    """
    The main function as the entry of this python script.
    """

    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description='Crop faces from pictures under the specified directory.')
    parser.add_argument(
        '-d',
        type=str,
        required=True,
        help='the directory of pictures to do face cropping')
    args = parser.parse_args()

    # Start cropping
    crop_faces_from_pictures(args.d)


if __name__ == '__main__':
    main()
    