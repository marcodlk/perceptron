"""
Created on Tue Aug 29 11:53:40 2017

@author: Kasey Hagi
@adapted by: Marco de Lannoy Kobayashi
"""
from random import randint

def generate_random_linear_separable(size=10,
                                     slope=[0,5],
                                     inter=[0,10],
                                     bounds=[-50,50]):
    _dataset = []
    _slope = randint(slope[0],slope[1])
    _yintercept = randint(inter[0],inter[1])

    for i in range(size):
        x0 = randint(bounds[0],bounds[1])
        x1 = randint(bounds[0],bounds[1])
        y = _slope*x0 + _yintercept
    
        while x1 == y:
            x1 = randint(bounds[0],bounds[1])
        if x1 > y :
            label = 1
        elif x1 < y:
            label = -1
        else : 
            label = 0
        _dataset.append([float(x0), float(x1),label])

    return _dataset


