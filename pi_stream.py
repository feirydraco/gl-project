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

#open("log.txt", "w").close()

buffer = None
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
curx, cury, curz =  0, 0, 0
prevx, prevy, prevz = 0, 0, 0
prevImage = None
OBS_LIMIT = 1
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
            current_data = str(curx) + " " + str(cury) + " " + str(theta) + " "
            with open("log.txt", "a") as file:
                file.write(current_data)
            
                

                
            # print("Previous:", prevx, prevy, prevz)
            # print((query["m_left"] * 100 + query["m_right"] * 100) / 2, query["dtheta"])
        

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


        corners = cv2.goodFeaturesToTrack(cv_image,25,0.01,10)
        corners = np.int0(corners)

        
        for i in corners:
            x,y = i.ravel()
            current_data += str(x) + " " + str(y) + " "
            cv2.circle(cv_image, (x,y),3,255,-1)
        
        cv2.imshow('Stream', cv_image)

        if buffer != contents:
            with open("log.txt", "a") as file:
                for i in corners:
                    x,y = i.ravel()
                    file.write(str(x) + " " + str(y) + " ")
            with open("log.txt", "a") as file:
                file.write("\n")

    

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        buffer = contents

finally:
    connection.close()
    server_socket.close()
