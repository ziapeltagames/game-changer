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
from deck import Deck
from resource import Resource, ResourceDie
from location import Location

class AchievementType(Enum):
    RESOURCE = 0
    OBSTACLE = 1
    
class AchievementDeck(Deck):    
    
    def __init__(self):
        self.achievements = []

class Achievement():

    def __init__(self, name, achievement_type):
        self.name = name
        self.achievement_type = achievement_type

# If enough resources are on locations of the correct type,
# this achievement will be completed
class TotalResourceAchievement(Achievement):
        
    def __init__(self, name, achievement_type, resource_type, total):
        super().__init__(name, achievement_type)
        self.resource_type = resource_type
        self.total = total
        
    def completed(self, locations):
        loc_total = 0
        for loc in locations:
            if loc.rpool.resource_type == self.resource_type:
                loc_total = loc_total + loc.rpool.total()
                
        if loc_total >= self.total:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.name} {self.resource_type} {self.total}'
        
if __name__ == "__main__":
    
    ach1 = TotalResourceAchievement('Gather Wood', AchievementType.RESOURCE, 
                                    Resource.TIMBER, 7)
    ach2 = TotalResourceAchievement('Gather Mana', AchievementType.RESOURCE, 
                                    Resource.MANA, 9)    
    
    size = random.randint(1, 6)
    loc1 = Location('Big Forest', Resource.TIMBER, size)
    loc1.add_die(ResourceDie(Resource.TIMBER))
    print(loc1)
    loc2 = Location('Little Forest', Resource.TIMBER, size)
    loc2.add_die(ResourceDie(Resource.TIMBER))
    print(loc2)
    loc3 = Location('Big Tower', Resource.MANA, size)
    loc3.add_die(ResourceDie(Resource.MANA))
    print(loc3)     
    loc4 = Location('Little Tower', Resource.MANA, size)
    loc4.add_die(ResourceDie(Resource.MANA))
    print(loc4)    
    
    locs = [loc1, loc2, loc3, loc4]
    
    print(ach1.completed(locs))
    print(ach2.completed(locs))