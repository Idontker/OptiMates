from random import *
import logging
import math
import numpy as np


class point:
    def __init__(self, v1, v2, v3, polar=True) -> None:
        """create a 3d point
        if polar == Ture: (v1,v2,v3) = (r,theta,phi)
        else            : (v1,v2,v3) = (x,y,z)
        default: polar = True
        all angels may be in radial form
        """
        if polar == True:
            self.r = v1
            self.phi = v2
            self.theta = v3
            self.recalcCartesian()
        else:
            self.x = v1
            self.y = v2
            self.z = v3
            self.recalcPolar()

    def __str__(self):
        return (
            "polar("
            + str(self.r)
            + ","
            + str(self.phi)
            + ","
            + str(self.theta)
            + ") == ["
            + str(self.x)
            + ","
            + str(self.y)
            + ","
            + str(self.z)
            + "]"
        )

    def recalcPolar(self):
        x, y, z = self.x, self.y, self.z
        self.r = math.sqrt(x * x + y * y + z * z)
        self.theta = np.arccos(z / self.r)

        if x > 0:
            self.phi = np.arctan(y / x)
        elif x == 0:
            self.phi = np.sign(y) * np.pi / 2
        else:  # x < 0
            if y >= 0:
                self.phi = np.arctan(y / x) + np.pi
            else:  #  y < 0
                self.phi = np.arctan(y / x) - np.pi
        pass

    def recalcCartesian(self):
        r, theta, phi = self.r, self.theta, self.phi
        self.x = r * math.sin(theta) * math.cos(phi)
        self.y = r * math.sin(theta) * math.sin(phi)
        self.z = r * math.sin(theta)
        pass

    def prod(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def dist(self, other):
        tmp = self.prod(other)
        tmp = tmp / (self.r * other.r)
        return np.arccos(tmp)


pass


def generateRandomPointOnSphere(r):
    theta = random() * np.pi
    phi = random() * 2 * math.pi
    return point(r, theta, phi)


def dist(p1, p2):
    tmp = p1.prod(p2)
    tmp = tmp / (p1.r * p2.r)
    return np.arccos(tmp)
