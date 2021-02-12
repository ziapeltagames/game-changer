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
        if self and other:
            return (self.value == other.value and
                    self.resource_type == other.resource_type)
        else:
            return False

    def __ne__(self, other):
        if self and other:
            return (self.value != other.value)
        else:
            return False

    def __lt__(self, other):
        return (self.value < other.value)

    def __le__(self, other):
        return (self.value <= other.value)

    def __gt__(self, other):
        return (self.value > other.value)

    def __ge__(self, other):
        return (self.value >= other.value)
    
class ResourcePool:
    
    def __init__(self, resource_type, pool_size, start_empty = False):
        self.resource_type = resource_type
        self.pool_size = pool_size
        self.dice = []
        
        if start_empty:
            return
        
        for i in range(pool_size):
            bisect.insort_left(self.dice, ResourceDie(resource_type))
            
    def total(self):
        total = 0
        for die in self.dice:
            total = total + die.value
        return total
    
    def refill(self):
        while len(self.dice) < self.pool_size:
            bisect.insort_left(self.dice, ResourceDie(self.resource_type))
            
    def capacity(self):
        return self.pool_size - len(self.dice)            
        
    # What is the highest valued die less than or equal to the given value?
    def highest_die_under(self, lvalue):
        i = bisect.bisect(self.dice, ResourceDie(self.resource_type, lvalue))
        if i > 0:
            return self.dice[i - 1]
        else:
            return None
        
    def lowest_die(self):
        if len(self.dice) > 0:
            return self.dice[0]
        else:
            return None
        
    def add(self, die):            
        bisect.insort_left(self.dice, die)
        
    def remove(self, die):
        self.dice.remove(die)
        
    def __iter__(self):
        return self.dice.__iter__()
    
if __name__ == "__main__":
    
    rp = ResourcePool(Resource.MANA, random.randint(1, 6))
    for nd in rp:
        print(nd)
        
    skill = random.randint(1, 6)
    highest_die = rp.highest_die_under(skill)
    print()
    print('Skill', skill, ': Highest Die', highest_die)