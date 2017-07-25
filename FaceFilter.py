mport os
import os.path 
import cv2
import numpy as np

def detectFace(parent, imageName):
    
    fileFullPath = os.path.join(parent,filename)
    print("filename with full path:"+ fileFullPath)  
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    destImageDir="./dest/tiantian"
    
    
    img = cv2.imread(fileFullPath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        print('face detected in %s' % fileFullPath)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            convert = 'convert {0} -crop {1[2]}x{1[3]}+{1[0]}+{1[1]} {2}'.format(fileFullPath, (x,y,w,h), destImageDir+'/'+filename)
            print(convert)
            os.system(convert)


if __name__ == '__main__':
    
    sourceDir="./images/tian"  
    for parent,dirnames,filenames in os.walk(sourceDir):  
        for filename in filenames:    
            #print("parent folder is:" + parent)  
            if(filename.endswith('.jpg')):
                detectFace(parent,filename)
            
            
            
            

   
