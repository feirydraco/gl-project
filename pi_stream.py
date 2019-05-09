import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
from ast import literal_eval
import urllib.request
import sys
import time

orb = cv2.ORB_create(25)

stream = cv2.VideoCapture(0)
img_id = 1

# Create some random colors
color = np.random.randint(0,255,(100,3))

buffer = None
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
curx, cury, curz =  0, 0, 0
prevx, prevy, prevz = 0, 0, 0
prevImage = None
observations = {}
# ref_image = cv2.imread("test.jpg")
# ref_image = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
accept_rate = 0 
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
        if buffer == contents:
            accept_rate += 1
            if accept_rate == 13:
                print("Current frame for pose generated.")
                accept_rate = 0
        if buffer != contents:
            query = literal_eval(contents)
            print(query)
            prevx = curx
            prevy = cury   
            prevz = curz
            curx = query["pose"][0]
            cury = query["pose"][1]
            theta = query["theta"]
            mleft = query["m_left"]
            mright = query["m_right"]
            TS = query["TS"]
            dtheta = query["dtheta"]
            curz = 0
            # time.sleep(1)
            # current_data = str(TS) + " " + str(curx) + " " + str(cury) + " " + str(theta) + " " + str(dtheta) + " " + str(mleft) + " " + str(mright) + " "
            # with open("log.txt", "a") as file:
            #     file.write(current_data)
            # print("Previous:", prevx, prevy, prevz)
            # print((query["m_left"] * 100 + query["m_right"] * 100) / 2, query["dtheta"])
        
       
        
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)
        
        cv_image = np.flip(np.flip(np.array(image), 0), 1)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        kp, des = orb.detectAndCompute(cv_image, None)
        # if (curx, cury, theta) not in observations:
        #     observations[(curx, cury, theta)] = (kp, des)
        # else:
            # create BFMatcher object
            # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            # # Match descriptors.
            # matches = bf.match(des, observations[(curx, cury, theta)][1])

            # # Sort them in the order of their distance.
            # matches = sorted(matches, key = lambda x:x.distance)
            # cv_image = cv2.drawKeypoints(cv_image, observations[(curx, cury, theta)][0], None, color=(0, 255, 0), flags=0)
            # for match in matches:
            #     print(match.distance)
        cv_image = cv2.drawKeypoints(cv_image, kp, cv_image, (0, 255, 0), flags=2)
        cv2.imshow("Stream", cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        buffer = contents
        prevImage = cv_image

finally:
    connection.close()
    server_socket.close()
