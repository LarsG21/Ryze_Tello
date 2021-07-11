import numpy as np
import cv2

def calc_area_bbox_percentage(w,h,shape):
    return np.round((w*h/(shape[0]*shape[1])*100),2)

def calc_face_center(x,y,w,h):
    return int(x+w/2),int(y+h/2)



def draw_rectangle(img, bbox, l=30, t=5, rt= 1, color = (0, 0, 255), text = 'IDEL'):
    x, y, w, h = bbox
    x1, y1 = x + w, y + h

    cv2.rectangle(img, bbox, color , rt)
    # Top Left  x,y
    cv2.line(img, (x, y), (x + l, y), color, t)
    cv2.line(img, (x, y), (x, y+l), color, t)
    # Top Right  x1,y
    cv2.line(img, (x1, y), (x1 - l, y), color, t)
    cv2.line(img, (x1, y), (x1, y+l), color, t)
    # Bottom Left  x,y1
    cv2.line(img, (x, y1), (x + l, y1), color, t)
    cv2.line(img, (x, y1), (x, y1 - l), color, t)
    # Bottom Right  x1,y1
    cv2.line(img, (x1, y1), (x1 - l, y1), color, t)
    cv2.line(img, (x1, y1), (x1, y1 - l), color, t)
    cv2.putText(img,text,(x,y+h+30),cv2.FONT_HERSHEY_PLAIN,3,color,thickness=2)
    return img

def check_hand_in_box(lmList, valid_rect):
    return lmList[5][1]>valid_rect[0] and lmList[17][1]<valid_rect[0]+valid_rect[2] and lmList[11][2]>valid_rect[1] and lmList[17][2]<valid_rect[1]+valid_rect[3]

optimal_area = 9 #%
def track_Face(me, area, center, shape, pid = [0.4,0.4,0.0001], pErrorX = 0, pErrorY = 0, pErrorZ = 0):
    image_width = shape[1]
    image_height = shape[0]

    x = center[0]
    y = center[1]
    z = area
    print(area)
    x_error = x - image_width / 2
    yv = pid[0] * x_error + pid[1] * (x_error - pErrorX)   #yaw
    yv = int(np.clip(yv,-100,100))

    y_error = y - image_height/2
    ud = pid[0] * y_error + pid[1] * (y_error - pErrorY)
    ud = int(np.clip(-ud, -100, 100))       #Inverted because drone is rotated 180°
    z_error = (z - optimal_area)*20     #TODO: Not optimal --> Area decreases only a little when drohne gets far away
    fb = pid[0] * z_error + pid[1] * (z_error - pErrorZ)        #TODO: Example 4% to 3% --> Increase speed if area < 4%
    if area < 1:
        fb = fb*2   #Increase speed if far away
    fb = int(np.clip(-fb, -30, 30)) #Inverted because drone is rotated 180°
    me.send_rc_control(0,fb,ud,yv)
    #print("FB:",fb,"Yaw:",yv,"Op/Down:",ud)
    #print("Ex:", x_error, "Ey:",y_error,"Ez:",z_error)
    return x_error, y_error, z_error