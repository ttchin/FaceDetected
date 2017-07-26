import cv2


cap = cv2.VideoCapture(0)
count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("./image_filter/before/frame%d.jpg" % count, frame)     # save frame as JPEG file
    count += 1

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    if count > 100:
        break
