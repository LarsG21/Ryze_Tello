from djitellopy import Tello
import cv2
from time import sleep

tello = Tello()

tello.connect()
print(tello.get_battery())
print()
tello.send_rc_control(0, 0, 0, 0)
tello.streamon()



while True:
    img = tello.get_frame_read().frame
    if img is not None:
        img_resize = cv2.resize(img,(640,480))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

