import KeyPressModule as kp
import djitellopy as Tello
import cv2

kp.initialize()
me = Tello.Tello()
me.connect()
me.streamon()
print("Battery:",me.get_battery(),"Temp:", me.get_temperature())

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


while True:
    print("Temp:", me.get_temperature())
    img = me.get_frame_read().frame
    if img is not None:
        pass
        img_resize = cv2.resize(img, (640, 480))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    lr, fb, up, yv = get_keyboard_input()
    me.send_rc_control(lr, fb, up, yv)

    if kp.getKey('l'):
        me.land()
    elif kp.getKey('t'):
        me.takeoff()
