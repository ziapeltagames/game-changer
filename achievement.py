# -*- coding: utf-8 -*-
"""
There are a wide variety of achievements possible, related to combinations
of resources as well as specific types and numbers of obstacles that
are overcome.

Created on Sun Aug 30 09:08:18 2020

@author: phill
"""

import random

from enum import Enum
from resource import Resource, ResourceDie, LocationResourceDie
from location import Location

# Used to find all the subsets that add or exceed a particular number
def subset_sum(loc_dice, target, partial = [], partial_sum = 0):
    
    if partial_sum >= target:
        yield partial, partial_sum
    for i, loc_die in enumerate(loc_dice):
        remaining = loc_dice[i + 1:]
        yield from subset_sum(remaining, target, partial + [loc_die], partial_sum + loc_die.die.value)
    
class AchievementType(Enum):
    
    SUM = 1
    SET = 2
    DISTINCT = 3    
    OBSTACLE = 4

class Achievement():

    def __init__(self, name, achievement_type):
        self.name = name
        self.achievement_type = achievement_type
        
    def encode(self):
        return [self.achievement_type.value]

# If enough resources are on locations of the correct type,
# this achievement will be completed
class SumResourceAchievement(Achievement):
        
    def __init__(self, name, achievement_type, resource_type, total):
        super().__init__(name, achievement_type)
        self.resource_type = resource_type
        self.total = total
        
    def __str__(self):
        return f'{self.name} {self.resource_type} {self.total}'       
    
    def __repr__(self):
        return self.__str__()
        
    # A simple hueristic to complete a sum achievemnt - will take the lowest
    # valued dice that equal or exceed the achievement total
    def completed(self, locations):
        
        ld = []
        
        for loc in locations:
            if loc.rpool.resource_type == self.resource_type:
                for die in loc.rpool:
                    ld.append(LocationResourceDie(die, loc))
        
        subsets = []
        for subset in subset_sum(ld, self.total):
            subsets.append(subset)
            
        subsets.sort(key = lambda tup: tup[1])
        
        if(subsets):
            return subsets[0]
        else:
            return False
        
    def encode(self):
        obs = super().encode()
        obs.append(self.resource_type.value)
        obs.append(self.total)
        return obs
        
if __name__ == "__main__":
    
    ach1 = SumResourceAchievement('Gather Wood', AchievementType.SUM, 
                                  Resource.TIMBER, 7)  
    
    size = random.randint(1, 2)
    loc1 = Location('Big Forest', Resource.TIMBER, size)
    for i in range(loc1.capacity()):
        loc1.add_die(ResourceDie(Resource.TIMBER))
    print(loc1)

    size = random.randint(1, 2)    
    loc2 = Location('Little Forest', Resource.TIMBER, size)
    for i in range(loc2.capacity()):
        loc2.add_die(ResourceDie(Resource.TIMBER))
    print(loc2)  
    
    locs = [loc1, loc2]
    
    print(ach1.completed(locs))
    
    print(ach1.encode())