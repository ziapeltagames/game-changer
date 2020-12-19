# -*- coding: utf-8 -*-
"""
There are a wide variety of achievements possible, related to combinations
of resources as well as specific types and numbers of obstacles that
are overcome.

Created on Sun Aug 30 09:08:18 2020

@author: phill
"""

from enum import Enum
from deck import Deck
from resource import Resource

class AchievementType(Enum):
    SUM = 0
    SET = 1
    STRAIGHT = 2
    OBSTACLE = 3
    
class AchievementDeck(Deck):    
    
    def __init__(self):
        self.achievements = []

class Achievement():

    def __init__(self, achievement_type):
        self.achievement_type = achievement_type

class ResourceAchievement(Achievement):

    def __init__(self, name):
        print('tbd')
        
if __name__ == "__main__":
    
    AchievementDeck()