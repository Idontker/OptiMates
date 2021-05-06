from random import *
import logging
import math
import numpy as np

class Point:
    def __init__(self, v1, v2, v3, polar=True) -> None:
        """create a 3d point
        if polar == Ture: (v1,v2,v3) = (r,theta,phi)
        else            : (v1,v2,v3) = (x,y,z)
        default: polar = True
        all angels may be in radial form
        """
        if polar == True:
            self.r = float(v1)
            self.phi = v2
            self.theta = v3
            self.recalcCartesian()
        else:
            self.x = v1
            self.y = v2
            self.z = v3
            self.recalcPolar()
        # logging.debug(self)

    def __str__(self):
        # return (
        #     "polar(" + str(self.r) + "," + str(self.phi) + "," + str(self.theta) + ")"
        # )
        return (
            "polar("
            + str(self.r)
            + ","
            + str(self.phi)
            + ","
            + str(self.theta)
            + ")\t == ["
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
        self.z = r * math.cos(theta)
        pass

    def prod(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def dist(self, other):
        if self == other:
            return 0
        tmp = self.prod(other)
        tmp = tmp / (self.r * other.r)
        return np.arccos(tmp)


pass

def parsePoint(s:str) -> Point:
    extract_polar = s.split("(")[1].split(")")[0].split(",")
    return Point(float(extract_polar[0]), float(extract_polar[1]), float(extract_polar[2]), polar=True)


def generateRandomPointOnSphere(R):
    theta = random() * np.pi
    phi = random() * 2 * math.pi
    return Point(R, theta, phi)


def dist(p1, p2):
    if p1 == p2:
        return 0
    tmp = p1.prod(p2)
    tmp = tmp / (p1.r * p2.r)
    return np.arccos(tmp)
