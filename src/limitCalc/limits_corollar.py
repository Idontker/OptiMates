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


def densapproach(mu, n, r):
    v = omega(r)
    fakt1 = 1 + 1 / (mu - 1)
    fakt2 = n * math.log(mu * n) + 1
    tmp = fakt1 * fakt2
    return 1 / v * fakt1 * fakt2


def generateMu(fak):
    if last_calc != -1:
        return last_calc + (random() - 0.5) / acc
    else:
        return random() * fak *5 + 1.5


def plot_dens(r, n, loops):
    data = pd.DataFrame(columns=["mu", "upper"])
    for i in range(1, loops):

        mu = generateMu(1)

        upper_limit = densapproach(mu, n, r)
        row = {"mu": mu, "upper": upper_limit}
        data = data.append(row, ignore_index=True)
        if i % 1000 == 0:
            print(i)
    data = data.sort_values(by="mu")
    sorted_min = data.sort_values(by="upper")
    return data, sorted_min


R = 1
t = 3.5 / 2
r = math.radians(t)
last_calc = -1
# last_calc = 1.999997782432965
acc = 100


LOW = lower(r)
print(LOW)
# print(UPPER)


################ TEST DENS #########################


sorted_mu, sorted_uppper = plot_dens(r, 2, 50_000)
UP = sorted_uppper.iloc[0]
print(
    "r:\t{}\nr/2:\t{}\nmu\t{}\ndelta:\t{}".format(r, r / 2, UP["mu"], r / 2 - UP["mu"])
)
print("lower:\t{}\nupper:\t{}".format(LOW, UP["upper"]))


sorted_uppper.plot(x="mu", y="upper")
plt.show()
sorted_mu.hist()
plt.show()
