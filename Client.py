import urllib.request
import numpy as np
import sys
from ast import literal_eval
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation


# fig, ax = plt.subplots()
# x, y = [], []
# ln, = plt.plot([], [], 'r-')
buffer = None

# def init():
#     ax.set_xlim(-10, 10)
#     ax.set_ylim(-10, 10)
#     return ln,

# def update(frame):
#     global buffer
#     try:
#         contents = urllib.request.urlopen("http://" + sys.argv[1]).read().decode()
#     except:
#         print("Server error.")
#         contents = None
#     if contents == None:
#         time.sleep(0.2)
#         print("Retrying..")
#     if buffer != contents:
#         try:
#             query = literal_eval(contents)
#             with open('helloworld.txt', 'w') as filehandle:  
#                 filehandle.write(query["pose"][0] + " " + query["pose"][1])
            
#             print(query["pose"][0], query["pose"][1])
#             x.append(query['pose'][0])
#             y.append(query['pose'][1])
#         except:
#             pass
#     buffer = contents
#     time.sleep(0.4)
#     ln.set_data(x, y)
#     return ln,

# ani = FuncAnimation(fig, update, init_func=init, blit=True)
# plt.show()

# print("Attempting to fetch data from:", sys.argv[1])
while(True):
    try:
        contents = urllib.request.urlopen("http://" + sys.argv[1]).read().decode()
    except:
        # print("oopsie")
        contents = None
    if contents == None:
        time.sleep(0.2)
        # print("Retrying..")
    if buffer != contents:
        try:
            query = literal_eval(contents)
            print(round(query["pose"][0], 6), round(query["pose"][1], 6), round(query["theta"], 6), sep =" ")
            x_pos = query["pose"][0]
            y_pos = query["pose"][1]
            plt.redraw()
        except:
            # print("error at", query)
            pass
    buffer = contents
    time.sleep(0.2)
