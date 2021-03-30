from math import *

PI: float = 3.14159265359
(a1, a2, a3, a4, a5) = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429)
sqrt2pi = sqrt(2 * pi)


def cnd(x):
    L = abs(x)
    K = 1.0 / (1.0 + 0.2316419 * L)
    K2 = K * K
    K3 = K2 * K
    K4 = K3 * K
    K5 = K4 * K
    w = 1.0 - 1.0 / sqrt2pi * exp(-L * L / 2.) * (a1 * K + a2 * K2 + a3 * K3 +
                                                  a4 * K4 + a5 * K5)
    if x < 0:
        w = 1.0 - w

    return w


def nd(x):
    return exp(-x * x / 2) / sqrt2pi
