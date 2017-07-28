#! encoding: UTF-8
import os
import os.path
import cv2
import sys
import numpy as np

def detectFace(parent, filename):

    fileFullPath = os.path.join(parent,filename)
    print("filename with full path:"+ fileFullPath)

    face_cascade = cv2.CascadeClassifier('opencv_config/haarcascade_frontalface_default.xml')
    destImageDir=os.path.join(os.path.dirname(sys.argv[0]),'image_filter','after')
    print(destImageDir)

    img = cv2.imread(fileFullPath)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # # ###########################
    # ret, thresh = cv2.threshold(img, 127, 255, 0)
    # contours, hierarchy = cv2.findContours(thresh, 1)
    # cnt = contours[0]
    # # x, y, w, h = cv2.boundingRect(cnt)
    #
    # # ###########################
    if len(faces) > 0:
        print('face detected in %s' % fileFullPath)
        for (x,y,w,h) in faces:
            crop_img = img[y:y+h,x:x+w]
            cv2.imwrite(os.path.join(destImageDir,filename),crop_img)


# if __name__ == '__main__':

sourceDir=destImageDir=os.path.join(os.path.dirname(sys.argv[0]),'image_filter')
print(sourceDir)
for parent,dirnames,filenames in os.walk(sourceDir):
    for filename in filenames:
        #print("parent folder is:" + parent)
        if(filename.endswith('.jpg')):
            detectFace(parent,filename)






