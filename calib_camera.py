import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

import sys
import time

nSnap   = 0
w       = 640
h       = 480
#open("log.txt", "w").close()

buffer = None
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        cv_image = np.flip(np.flip(np.array(image), 0), 1)
        
        print("Saving image ", nSnap)
        cv2.imwrite("./calib_files/{}.jpg".format(nSnap), cv_image)
        nSnap += 1
        # time.sleep(5)


        cv2.imshow('Stream', cv_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        

finally:
    connection.close()
    server_socket.close()
