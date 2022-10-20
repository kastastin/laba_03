import sys
import numpy as np
sys.path.append('../laba_03')
from FunRand import FunRand


class Element:
    id = 0
    def __init__(self, name = None, delay_mean = 1., delay_dev = 0., distribution = '', p = None, n_channel = 1):
        self.p = p
        self.id = Element.id
        Element.id += 1
        self.name = f'element_{self.id}' if name is None else name
        self.delay_mean = delay_mean # середня часова затримка
        self.delay_dev = delay_dev # значення середнього квадратичного відхилення часової затримки
        self.distribution = distribution
        self.quantity = 0
        self.tcurr = 0 # поточний момент часу
        self.next_elements = None
        self.n_channel = n_channel
        self.tnexts = [0.0] * self.n_channel # список моментів часу наступних подій
        self.states = [0] * self.n_channel
        
    # розрахунок часової затримки
    def get_delay(self):
        if self.distribution == 'exp':
            return FunRand.exp(self.delay_mean)
        elif self.distribution == 'unif':
            return FunRand.unif(self.delay_mean, self.delay_dev)
        elif self.distribution == 'norm':
            return FunRand.norm(self.delay_mean, self.delay_dev)
        elif self.distribution == 'erlanga':
            return FunRand.erlanga(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean
        
    # вхід в елемент
    def in_act(self):
        pass
    
    # вихід з елементу
    def out_act(self):
        self.quantity += 1
        
    def print_statistic(self):
        print(f'{self.name}: Quantity = {self.quantity}, State = {self.states};')

    def print_info(self):
        print(f'{self.name}: Quantity={self.quantity}, State={self.states}, tnext={np.round(self.tnexts, 9)}')
        
    def find_curr_channels(self):
        curr_channels = []
        for i in range(self.n_channel):
            if self.tnexts[i] == self.tcurr:
                curr_channels.append(i)
        return curr_channels
    
    def find_empty_channels(self):
        empty_channels = []
        for i in range(self.n_channel):
            if self.states[i] == 0:
                empty_channels.append(i)
        return empty_channels

    def do_statistics(self, delta):
        pass