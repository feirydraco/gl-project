import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
from visual_odometry import PinholeCamera, VisualOdometry
from ast import literal_eval
import urllib.request
import sys
import time

orb = cv2.ORB_create(25)
cam = PinholeCamera(640.0, 480.0, 360.0000, 718.8560, 607.1928, 185.2157)
vo = VisualOdometry(cam)
traj = np.zeros((600,600,3), dtype=np.float32)
stream = cv2.VideoCapture(0)
img_id = 1

buffer = None
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
curx, cury, curz =  0, 0, 0
prevx, prevy, prevz = 0, 0, 0
prevImage = None
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        
        try:
            contents = urllib.request.urlopen("http://" + sys.argv[1]).read().decode()
        except:
            contents = None
        if contents == None:
            pass
        elif buffer != contents:
            query = literal_eval(contents)
            # curx = query["pose"][0]
            # cury = query["pose"][1]
            # curz = 0
            # print(x_pos, y_pos, z_pos)
            # if curx is None and cury is None and curz is None:
            #     curx = query["pose"][0]
            #     cury = query["pose"][1]
            #     curz = 0
            # else:
            prevx = curx
            prevy = cury   
            prevz = curz
            curx = query["pose"][0]
            cury = query["pose"][1]
            theta = query["theta"]
            curz = 0
            print("Current:", curx, cury, curz, theta)
            print("Previous:", prevx, prevy, prevz)
        buffer = contents

        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        cv_image = np.flip(np.flip(np.array(image), 0), 1)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        vo.setScale(curx, cury, curz, prevx, prevy, prevz)
        vo.update(cv_image)
        cur_t = vo.cur_t
        if(img_id > 2):
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0., 0., 0.

        draw_x, draw_y = int(x)+290, int(z)+90
        true_x, true_y = int(vo.x)+290, int(vo.z)+90

        cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
        cv2.circle(traj, (true_x,true_y), 1, (0,0,255), 2)
        cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
        cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

        cv2.imshow('Road facing camera', cv_image)
        cv2.imshow('Trajectory', traj)
        cv2.waitKey(1)
        img_id += 1
        corners = cv2.goodFeaturesToTrack(cv_image,25,0.01,10)
        # kp = orb.detect(cv_image, None)
        # kp, des = orb.compute(cv_image, kp)
        corners = np.int0(corners)
        for i in corners:
            x,y = i.ravel()
            print(x, y)
            cv2.circle(cv_image,(x,y),3,255,-1)
        # img = np.zeros((cv_image.shape[0], cv_image.shape[1]))
        # img = cv2.drawKeypoints(cv_image, kp, img, color=(0,255,0), flags=0)
        cv2.imshow('Stream', cv_image)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()
