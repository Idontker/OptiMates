import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
import pandas as pd


def vol(r):
    return 2 * R * R * math.pi * (1 - math.cos(r))


def omega(r):
    full = 4 * R * R * math.pi
    part = vol(r)
    return part / full


def lower(r):
    small = omega(r)
    return 1 / small


def upper(r, epsi):
    omega_r_e = omega(r - epsi)
    omega_e = omega(epsi)
    tmp = math.log(omega_r_e / omega_e) + 1
    # print("r-e:{}       e:{}      log:{}".format(omega_r_e, omega_e, tmp))
    tmp = tmp / omega_r_e
    return tmp


def test_upper(r, loops):
    min_upper = upper(r, r / 4)
    val = r / 4
    for i in range(1, loops):
        epsi = random()
        while epsi >= r / 2:
            epsi = random()
        upper_limit = upper(r, epsi)
        if min_upper > upper_limit:
            min_upper = upper_limit
            val = epsi
            print("{}           {}          {}".format(val, min_upper, min_upper - LOW))
    return min_upper


def generateEpsi(r):
    if last_calc != -1:
        return last_calc + (random() - 0.5) * last_calc
    else:
        return random() * r / 2


def plot_upper(r, loops):
    data = pd.DataFrame(columns=["epsi", "upper"])
    for i in range(1, loops):

        epsi = generateEpsi(r)
        while epsi >= r / 2:
            epsi = generateEpsi(r)

        upper_limit = upper(r, epsi)
        row = {"epsi": epsi, "upper": upper_limit}
        data = data.append(row, ignore_index=True)
        if i % 1000 == 0:
            print(i)
    data = data.sort_values(by="epsi")
    sorted_min = data.sort_values(by="upper")
    return data, sorted_min


R = 1
t = 3.5 / 2
r = math.radians(t)
last_calc = -1
# last_calc = 0.015271623959604528
acc = 100


LOW = lower(r)
print(LOW)

sorted_epsi, sorted_uppper = plot_upper(r, 50_000)
UP = sorted_uppper.iloc[0]


print(
    "r:\t{}\nr/2:\t{}\nepsi\t{}\ndelta:\t{}".format(
        r, r / 2, UP["epsi"], r / 2 - UP["epsi"]
    )
)
print("lower:\t{}\nupper:\t{}".format(LOW, UP["upper"]))


sorted_uppper.plot(x="epsi", y="upper")
plt.show()
sorted_epsi.hist()
plt.show()


# print(test_upper(r,10_000_000))
