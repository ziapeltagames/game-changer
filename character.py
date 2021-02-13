# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:02:54 2020

@author: phill
"""

from enum import Enum

class Skill(Enum):
    COMMAND = 0
    DISGUISE = 1
    LORE = 2
    RAPPORT = 3
    COMBAT = 4
    TACTICS = 5
    THIEVERY = 6
    SURVIVAL = 7
    
class Character:
    
    def __init__(self, name, command = 3, disguise = 3,
                 lore = 3, rapport = 3, combat = 3, tactics = 3,
                 thievery = 3, survival = 3):
        self.name = name
        self.skills = {}
        self.skills[Skill.COMMAND] = command
        self.skills[Skill.DISGUISE] = disguise
        self.skills[Skill.LORE] = lore
        self.skills[Skill.RAPPORT] = rapport
        self.skills[Skill.COMBAT] = combat
        self.skills[Skill.TACTICS] = tactics
        self.skills[Skill.THIEVERY] = thievery
        self.skills[Skill.SURVIVAL] = survival
        self.location = None
    
    def __str__(self):
        loc_string = f'{self.name} '
        for r in self.skills:
            loc_string += str(r) + ':' + str(r.value) + ' '
        return loc_string
    
if __name__ == "__main__":
    
    ch = Character('Oniri')
    print(ch)