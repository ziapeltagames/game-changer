# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:02:54 2020

@author: phill
"""

import random
from enum import Enum

class Resource(Enum):
    MANA = 0
    TIMBER = 1
    ORE = 2
    LUXURY = 3
    FOOD = 4

class ResourceDie:
    
    def __init__(self, resource_type):
        self.resource_type = resource_type
        self.value = random.randint(1, 6)
    
    def roll(self):
        self.value = random.randint(1, 6)
    
class ResourcePool:
    
    def __init__(self, resource_type, pool_size):
        self.resource_type = resource_type
        self.pool_size = pool_size
        self.dice = []
        for i in range(pool_size):
            self.dice.append(ResourceDie(resource_type))
            
    def refill(self):
        while len(self.dice) < self.pool_size:
            self.dice.append(ResourceDie(self.resource_type))
            
    def remove(self, die):
        self.dice.remove(die)
    
if __name__ == "__main__":
    
    rd = ResourceDie(Resource.MANA)
    print(rd.resource_type, rd.value)
    rd.roll()
    print(rd.resource_type, rd.value)
    
    rp = ResourcePool(Resource.MANA, 4)
    print(rp.dice)