# import numpy as np
from pylab import *
# # from sympy import symbols, Matrix

# obs = np.array((571, 260, 1))
# print(obs)
K = array([[1.112718502113158593e+03,0.000000000000000000e+00,3.261312488982279092e+02], \
            [0.000000000000000000e+00,1.109070993342474367e+03,2.284030377231190130e+02], \
            [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])


# print("K:", np.linalg.inv(K))
# trans_obs = np.dot(K, obs)
# print("trans_obs:", trans_obs)
# pose = np.array((0.1194394679385664, -0.019075016497666727, 0.0, 1))
# print("pose:", pose)
# pose = np.reshape(pose, (4, 1))
# print(pose)
# print(np.dot(trans_obs, pose))

# K = array([[5,0,0],[0,5,0],[0,0,1]])
def plotpoints(k):
    th = k*pi/16
    XYZ=array([(5*i,5*j*cos(th),50+5*j*sin(th)) for i in range(-2,3) for j in range(-2,3)]).T
    print(XYZ)
    xys = dot(K,XYZ)
    xy = 1.0*xys[:2,:]/xys[-1,:]
    plot(xy[0], xy[1], 'o')
    axis('equal')
plotpoints(1)
show()