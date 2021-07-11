from djitellopy import Tello
import cv2
from time import sleep
import cvzone

tello = Tello()

tello.connect()
print("Battery:",tello.get_battery(),"Temp:", tello.get_temperature())
tello.send_rc_control(0, 0, 0, 0)
sleep(2)
tello.takeoff()
sleep(2)
tello.send_rc_control(0, 50, 0, 0)
#tello.rotate_counter_clockwise(90)
sleep(2)
tello.send_rc_control(0, -50, 0, 0)
sleep(2)
tello.rotate_clockwise(90)
sleep(2)
tello.send_rc_control(0, 0, 0, 0)
tello.land()


# tello.move_forward(20)
# sleep(2)


# tello.move_back(20)

# tello.land()
