import KeyPressModule as kp
import djitellopy as Tello
import cv2
import cvzone
import numpy as np
import Utils
import FaceTrackingModule as ftm
import HandTrackingModule as htm
import logging
import time
from threading import Thread

logging.basicConfig(filename="logfile.log",level=logging.DEBUG)

####################################Parameters############################

lr, fb, ud, yv = 0, 0, 0, 0
center = 0,0
pid = [0.1,0.4,0.0001]
pErrorX = 0
pErrorY = 0
pErrorZ = 0

STATUS = 'IDLE'
TIMER_RUNNING = False
wait_time  = 0
TIME_IS_UP = False

inner_forward_backward_range = [7, 10]

optimal_area = 9 # %

valid_rect =[0,0,0,0]

testing = False

def no_face_timer():
    print("Timer start")
    global TIMER_RUNNING
    global TIME_IS_UP
    global wait_time
    TIMER_RUNNING = True
    for wait_time in range(10):
        time.sleep(1)
    TIME_IS_UP = True


if testing:
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

if not testing:
    kp.initialize()
    me = Tello.Tello()
    me.connect()
    me.streamon()
    print("Battery:",me.get_battery(),"Temp:", me.get_temperature())
    #t1 = Thread(target=no_face_handler(me))


FPS_Counter = cvzone.FPS()

FaceDetector = ftm.FaceDetector(minDetectionCon=0.75,model_selection=1)
HandDetector = htm.handDetector(trackCon=0.85)



color=(0,0,255)
fingers = [0,0,0,0,0]

while True:

    if testing:
        success, img = cap.read()
    else:
        img = me.get_frame_read().frame
    if img is not None:
        img_resize = cv2.resize(img, (1280, 720))
        img_resize, faces = FaceDetector.findFaces(img_resize, draw=True)

        if len(faces) != 0:
            TIMER_RUNNING = False   #Reset no_face_timer when face detected
            TIME_IS_UP = False
            wait_time = 0
            bbox = faces[0][1]
            #print(bbox)
            area = Utils.calc_area_bbox_percentage(bbox[2], bbox[3],img_resize.shape)
            center = Utils.calc_face_center(bbox[0], bbox[1], bbox[2], bbox[3])
            #print("Center = ", str(center), "Area = ", str(area))
            cv2.circle(img_resize,center,5,(255,0,255),cv2.FILLED)
            valid_rect = [bbox[0]-bbox[2]-int(bbox[2]*0.8),bbox[1],int(bbox[2]*1.2), int(bbox[3]*1.8)]
            img = Utils.draw_rectangle(img_resize, bbox= valid_rect,color=color,text=STATUS)

            if not testing and STATUS == 'TRACKING':
                pErrorX,pErrorY,pErrorZ = Utils.track_Face(me, area=area ,center=center, shape= img.shape,pid=pid,pErrorX= pErrorX, pErrorY=pErrorY, pErrorZ=pErrorZ)
            elif not testing and STATUS == 'WAITING':
                me.send_rc_control(0,0,0,0)

        else:
            #TODO: If no Face detected for 5 sec --> land
            #me.send_rc_control(0,0,0,0)
            if STATUS == 'TRACKING':
                if not TIMER_RUNNING and not TIME_IS_UP:
                    #me.send_rc_control(0, 0, 0, 0)
                    logging.info("Started Timer")
                    t1 = Thread(target=no_face_timer)
                    t1.start()
                elif TIMER_RUNNING and not TIME_IS_UP:
                    #me.send_rc_control(0, 0, 0, 0)
                    print("Wainting for face")
                elif TIMER_RUNNING and TIME_IS_UP:
                    TIMER_RUNNING = False
                    TIME_IS_UP = False
                    STATUS = 'LANDING'
                    logging.info("Landing because of timer")
                    print("TIMERS OUT AND LANDING! ")
                    me.land()

        img_resize = HandDetector.findHands(img_resize,draw=True)
        lmList, bbox_hand = HandDetector.findPosition(img_resize,handNo=0)
        if len(lmList) != 0:
            if Utils.check_hand_in_box(lmList,valid_rect):
                fingers = HandDetector.fingersUp()
                color=(0,255,0)
                if fingers == [1,1,1,1,1] and STATUS != 'LANDING':
                    logging.info("Landing Gesture")
                    print("Landing")
                    STATUS = 'LANDING'
                    me.land()
                elif fingers == [0,1,0,0,0] and STATUS != 'WAITING':
                    logging.info("Waiting Gesture")
                    STATUS = 'WAITING'
                elif fingers == [0,1,1,0,0] and STATUS != 'TRACKING':
                    logging.info("Tracking Gesture")
                    STATUS = 'TRACKING'
                elif fingers == [0,1,1,1,0]:
                    logging.info("Turuning Gesture")        #TODO: Evaluate this
                    me.rotate_clockwise(360)
            else:
                color=(0,0,255)
        else:
            color=(0,0,255)
        print("STATUS: ", STATUS)
        FPS_Counter.update(img_resize)
        cv2.circle(img_resize,(int(img_resize.shape[1]/2),int(img_resize.shape[0]/2)),5,(255,0,255),cv2.FILLED)
        cv2.line(img,(int(img_resize.shape[1]/2),int(img_resize.shape[0]/2)),center,(255,0,255))
        cv2.imshow("Image", img_resize)
        cv2.waitKey(1)

    if not testing:
        if kp.getKey('l'):
            logging.info("Manual landing")
            STATUS = 'LANDING'
            me.land()
            print("LANDING!!!!!!!")
        elif kp.getKey('t'):
            logging.info("Manual takeoff")
            STATUS = 'TRACKING'
            me.takeoff()
            time.sleep(1)
            me.go_xyz_speed(0,0,80,30)
            print("move up")
            time.sleep(1)
