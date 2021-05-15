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
    
    def __repr__(self):
        return self.__str__()    
        
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
    
# A resource die aware of the location it comes from - useful for sorting
# algorithms where combinations of dice summing to a total are found, and
# removed from associated location or resource pools
class LocationResourceDie():
    
    def __init__(self, die, location):
        self.die = die
        self.location = location
        
    def __str__(self):
        return f"{self.die.resource_type} {self.die.value} {self.location.name}"        
     
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.die.__eq__(other)

    def __ne__(self, other):
        return self.die.__ne__(other)

    def __lt__(self, other):
        return self.die.__lt__(other)

    def __le__(self, other):
        return self.die.__le__(other)

    def __gt__(self, other):
        return self.die.__gt__(other)

    def __ge__(self, other):
        return self.die.__ge__(other)       
    
class ResourcePool:
    
    def __init__(self, resource_type, pool_size, start_empty = False):
        self.resource_type = resource_type
        self.pool_size = pool_size
        self.dice = []
        
        if start_empty:
            return
        
        for i in range(pool_size):
            bisect.insort_left(self.dice, ResourceDie(resource_type))
        
    def __iter__(self):
        return self.dice.__iter__()
            
    def __str__(self):
        res_string = f'{self.resource_type.name}({self.pool_size}): '
        for r in self.dice:
            res_string += str(r.value) + ' '
        return res_string
    
    def __repr__(self):
        return self.__str__()   
    
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
        
    # Returns an encoding for the resource pool that can be returned
    # for Open AI Gym. The encoding is an integer for the resource
    # type (0-4), along with an integer for each die on the location (1-6)
    # up to capacity
    def encode(self):
        obs = [self.resource_type.value]
        
        for nd in self.dice:
            obs.append(nd.value)
                    
        for i in range(self.pool_size - len(self.dice)):
            obs.append(0)
        
        return obs        

    
if __name__ == "__main__":
    
    rp = ResourcePool(Resource.MANA, random.randint(1, 6))
    print(rp)
        
    skill = random.randint(1, 6)
    highest_die = rp.highest_die_under(skill)
    print()
    print('Skill', skill, ': Highest Die', highest_die)