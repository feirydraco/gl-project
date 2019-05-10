from filterpy.kalman import ExtendedKalmanFilter as EKF
import numpy as np
import time
import re
import sympy
import math
import cv2
import os
import time
from visual_odometry import PinholeCamera, VisualOdometry

cam = PinholeCamera(640.0, 480.0, 1.112718502113158593e+03, 1.109070993342474367e+03, 3.261312488982279092e+02, 2.284030377231190130e+02)
vo = VisualOdometry(cam)
color = np.random.randint(0,255,(100,3))


lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

traj = np.zeros((600,600,3), dtype=np.uint8)
img_id = 1

def getObs(idx):
		curr = 0
		with open("log.txt") as log:
			for action in log:
				if curr == idx:
					return [action.split(" ")[i] for i in range(8)]
				curr += 1

for img_id in range(1, 32):
    try:
        vo.update(img_id)
    except:
        break
    cur_t = vo.cur_t
    if(img_id > 2):
        x, y, z = cur_t[0], cur_t[1], cur_t[2]
    else:
        x, y, z = 0., 0., 0.
    draw_x, draw_y = int(x)+290, int(z)+90
    true_x, true_y = int(vo.trueX)+290, int(vo.trueZ)+90

    cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
    cv2.circle(traj, (true_x,true_y), 1, (0,0,255), 2)
    cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
    text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
    cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)
    img = getObs(img_id)[7].strip()
    img = cv2.imread(os.path.abspath(img))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(img,(x,y),3,255,-1)
        Rx = true_x - 290
        Ry = true_y - 90
        Rz = np.sqrt((true_x + 100) ** 2 + (true_y + 100) ** 2)
        print("Point at:", Rx, Ry, Rz)
        with open("plot.txt", "a") as file:
                 file.write(str((true_x  - 290) * 100) + " " + str((true_y - 90) * 100) + " " + str((true_x - 290 + 2) * 100 / 640) + " " + str((true_y - 90 + 2) * 100 / 480) + " " + str(1) + "\n")

    cv2.imshow('Road facing camera', img)
    cv2.imshow('Trajectory', traj)
    cv2.waitKey(1)
    img_id += 1
    time.sleep(0.2)

cv2.imwrite('map.png', traj)






    