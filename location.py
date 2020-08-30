# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:07:53 2020

@author: phill
"""

class Location:
    
    def __init__(self, type):
        self.type = type
        self.resources = []
        self.characters = []
        
    def add_resource(self, resource):
        self.resources.append(resource)
        
    def add_character(self, character):
        self.characters.append(character)
        
    def get_resource(self, resource):
        print('tbd')
    
    def rm_character(self, character):
        print('tbd')
        
if __name__ == "__main__":
    
    loc = Location('Dreadmire')