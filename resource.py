# -*- coding: utf-8 -*-
"""
Tracks the community resource pools as sorted lists of resource dice,
along with utilities for handling resource types and resource dice.

Created on Sat Aug 29 11:02:54 2020

@author: phill
"""

import bisect
import random
from enum import Enum

class Resource(Enum):
    MANA = 0
    TIMBER = 1
    ORE = 2
    LUXURY = 3
    FOOD = 4

class ResourceDie:
    
    def __init__(self, resource_type, resource_value = None):
        self.resource_type = resource_type
        if resource_value:
            self.value = resource_value
        else:
            self.value = random.randint(1, 6)
    
    def roll(self):
        self.value = random.randint(1, 6)
        
    def __str__(self):
        return f"{self.resource_type} {self.value}"
        
    def __eq__(self, other):
        return (self.value == other.value and
                self.resource_type == other.resource_type)

    def __ne__(self, other):
        return (self.value != other.value)

    def __lt__(self, other):
        return (self.value < other.value)

    def __le__(self, other):
        return (self.value <= other.value)

    def __gt__(self, other):
        return (self.value > other.value)

    def __ge__(self, other):
        return (self.value >= other.value)
    
class ResourcePool:
    
    def __init__(self, resource_type, pool_size):
        self.resource_type = resource_type
        self.pool_size = pool_size
        self.dice = []
        for i in range(pool_size):
            bisect.insort_left(self.dice, ResourceDie(resource_type))
            
    def refill(self):
        while len(self.dice) < self.pool_size:
            bisect.insort_left(self.dice, ResourceDie(self.resource_type))
        
    # What is the highest valued die for the given skill?
    def highest_die(self, skill):
        i = bisect.bisect(self.dice, ResourceDie(self.resource_type, skill))
        if i > 0:
            return self.dice[i - 1]
        else:
            return None
        
    def lowest_die(self):
        if len(self.dice) > 0:
            return self.dice[0]
        else:
            return None
        
    def remove(self, die):
        self.dice.remove(die)
        
    def __iter__(self):
        return self.dice.__iter__()
    
if __name__ == "__main__":
    
    rp = ResourcePool(Resource.MANA, random.randint(1, 6))
    for nd in rp:
        print(nd)
        
    skill = random.randint(1, 6)
    highest_die = rp.highest_die(skill)
    print()
    print('Skill', skill, ': ', highest_die)