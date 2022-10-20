import numpy as np


# Generates a random value according to an exponential distribution
class FunRand:
    @staticmethod
    def erlanga(time_mean, k):
        return np.random.gamma(shape = k, scale = time_mean / k)

    @staticmethod
    def exp(time_mean):
        a = 0
        while a == 0:
            a = np.random.rand()
        return -time_mean * np.log(a)
    
    @staticmethod
    def unif(time_min, time_max):
        a = 0
        while a == 0:
            a = np.random.rand()
        a = time_min + a * (time_max - time_min)
        return a
    
    @staticmethod
    def norm(time_mean, time_diversion):
        return np.random.normal(loc = time_mean, scale = time_diversion)