from filterpy.kalman import ExtendedKalmanFilter as EKF
import numpy as np
import time
import re
import sympy
import math

# log = open("log.txt", "r")


class RobotEKF(EKF):
    def __init__(self, filename):
        EKF.__init__(self, dim_x = 3, dim_z = 2, dim_u = 2)
        self.TS = None
        self.obs_x = None
        self.obx_y = None
        self.obs_theta = None
        self.dtheta = None
        self.mleft = None
        self.mright = None
        self.distance_computed = None
        self.theta_computed = None
        self.s_t = None
        self.theta_t = None
        self.logfile = filename
        self.initvalues()
        B = 5
        self.setFxuParams()

        EKF.F = np.array([
            [self.s_t * math.cos(self.s_t + self.theta_t / 2)],
            [self.s_t * math.sin(self.s_t + self.theta_t / 2)],
            [self.theta_t],
        ])
        print(EKF.F)
        # self.F_j = self.fxu.jacobian(Matrix([x, y, theta]))
        # self.V_j = self.fxu.jacobian(Matrix([v, a]))

        # # save dictionary and it's variables for later use
        # self.subs = {x: 0, y: 0, v:0, a:0, 
        #              time:dt, w:wheelbase, theta:0}
        # self.x_x, self.x_y, = x, y 
        # self.v, self.a, self.theta = v, a, theta

    def setFxuParams(self):
        self.s_t = (float(self.mright) + float(self.mleft)) / 2
        self.theta_t = (float(self.mright) - float(self.mleft)) / 5

    def initvalues(self):
        with open(self.logfile) as log:
            for action in log:
                self.TS = action.split(" ")[0]
                self.obs_x = action.split(" ")[1]
                self.obx_y = action.split(" ")[2]
                self.obs_theta = action.split(" ")[3]
                self.dtheta = action.split(" ")[4]
                self.mleft = action.split(" ")[5]
                self.mright = action.split(" ")[6]
                self.image = action.split(" ")[7]
                break

    def returnTS(self, TS):
        with open(self.logfile) as log:
            for actions in log:
                print(actions)


if __name__ == "__main__":
    R = RobotEKF("log.txt")
    print(R.TS, R.obs_x, R.obx_y)
    