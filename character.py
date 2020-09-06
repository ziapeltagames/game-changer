# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 11:02:54 2020

@author: phill
"""

class Character:
    
    def __init__(self, name, command = 3, disguise = 3,
                 lore = 3, rapport = 3, combat = 3, tactics = 3,
                 thievery = 3, survival = 3):
        self.name = name
        self.command = command
        self.disguise = disguise
        self.lore = lore
        self.rapport = rapport
        self.combat = combat
        self.tactics = tactics
        self.thievery = thievery
        self.survival = survival
        self.location = None
    
if __name__ == "__main__":
    
    ch = Character('Oniri')
    print(ch)