import KeyPressModule as kp
import djitellopy as Tello
import cv2
import numpy as np

#################Parameters###########################
fSpeed = 117/10 # cm/s Forward speed    (15cm/s set)
aSpeed = 360/10 # deg/s Angular speed
intervall = 0.25 # s

distance_intervall = fSpeed*intervall   #cm
angular_intervall = aSpeed*intervall    #deg
#####################################################

testing = True
kp.initialize()
if not testing:

    me = Tello.Tello()
    me.connect()
    me.streamon()
    print("Battery:",me.get_battery(),"Temp:", me.get_temperature())

x,y = 300,300
angle = 0
distance = 0

def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50
    if kp.getKey('w'):
        fb = speed
    elif kp.getKey('s'):
        fb = -speed
    if kp.getKey('a'):
        lr = -speed
    elif kp.getKey('d'):
        lr = speed
    if kp.getKey('h'):
        ud = speed
    elif kp.getKey('b'):
        ud = -speed
    if kp.getKey('q'):
        yv = -speed
    elif kp.getKey('e'):
        yv = speed


    return lr, fb, ud, yv

def draw_points(img):
    cv2.circle(img,(x,y),2,(255,0,255),cv2.FILLED)


while True:
    img = np.zeros((600,600,3),np.uint8)
    draw_points(img)
    cv2.imshow("Map",img)
    lr, fb, ud, yv = get_keyboard_input()
    y=int(y-(fb*distance_intervall/100))
    x=int(x+(lr*distance_intervall/100))
    print(x,y)
    cv2.waitKey(1)

