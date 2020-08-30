# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:02:54 2020

@author: phill
"""

import random
from enum import Enum

class Resource(Enum):
    MANA = 1
    TIMBER = 2
    ORE = 3
    LUXURY = 4
    FOOD = 5

class ResourceDie:
    
    def __init__(self, type):
        self.type = type
        self.value = random.randint(1, 6)
    
    def roll(self):
        self.value = random.randint(1, 6)
    
class ResourcePool:
    
    def __init__(self, type, max):
        self.type = type
        self.max = max
        self.dice = []
        for i in range(max):
            self.dice.append(ResourceDie(type))
    
if __name__ == "__main__":
    
    rd = ResourceDie(Resource.MANA)
    print(rd.type, rd.value)
    rd.roll()
    print(rd.type, rd.value)
    
    rp = ResourcePool(Resource.MANA, 4)
    print(rp.dice)