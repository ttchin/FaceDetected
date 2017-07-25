import cv2
from boss_train import Model


if __name__ == '__main__':
    frame = cv2.imread('./w.jpg')
    cascade_path = "./opencv_config/haarcascade_frontalface_default.xml"
    model = Model()
    model.load()
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

    if len(facerect) > 0:
        print('face detected')
        color = (255, 255, 255)  # 白
        for rect in facerect:
            x, y = rect[0:2]
            width, height = rect[2:4]
            image = frame[y - 10: y + height, x: x + width]

            result = model.predict(image)
            if result == 0:  # boss
                print('Boss is approaching')

            else:
                print('Not boss')


