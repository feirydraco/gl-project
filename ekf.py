from filterpy.kalman import ExtendedKalmanFilter as EKF
import numpy as np
import time
import re
import sympy
import math

# np.array([
#             [self.s_t * math.cos(self.s_t + self.theta_t / 2)],
#             [self.s_t * math.sin(self.s_t + self.theta_t / 2)],
#             [self.theta_t],
  

#     def initvalues(self):
#         with open(self.logfile) as log:
#             for action in log:
#                 self.TS = action.split(" ")[0]
#                 self.obs_x = action.split(" ")[1]
#                 self.obx_y = action.split(" ")[2]
#                 self.obs_theta = action.split(" ")[3]
#                 self.dtheta = action.split(" ")[4]
#                 self.mleft = action.split(" ")[5]
#                 self.mright = action.split(" ")[6]
#                 self.image = action.split(" ")[7]
#                 break

#     def returnTS(self, TS):
#         with open(self.logfile) as log:
#             for actions in log:
#                 print(actions)


# if __name__ == "__main__":
#     R = RobotEKF("log.txt")
#     print(R.TS, R.obs_x, R.obx_y)
#get observation id, frame and values
def getObs(idx):
    curr = 0
    with open("log.txt") as log:
        for action in log:
            if curr == idx:
                return [action.split(" ")[i] for i in range(8)]
            else:
                curr += 1

R = EKF(3, 2, 2)
# R.x = [0 0 0]
R.x = np.array([initvalues()[1], initvalues()[2], initvalues()[3]])
print(getObs(0))





    