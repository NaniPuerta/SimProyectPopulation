import numpy as np
from math import log, sqrt, cos, pi

#random variables generation
#exponential distribution
def gen_exp(lambd):
    u = np.random.uniform()
    return -(1/lambd)*log(1-u)

#normal distribution
def gen_normal(mean=0, var=1):
    u1 = np.random.uniform()
    u2 = np.random.uniform()
    norm = sqrt(-2*log(u1))*cos(2*pi*u2)
    return norm*sqrt(var) + mean