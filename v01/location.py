# -*- coding: utf-8 -*-
"""
Locations have a name, resource types, and a maximum number of resource dice
they can hold.

Created on Sun Aug 30 09:07:53 2020

@author: phill
"""

import random
from resource import Resource, ResourceDie, ResourcePool

class Location:
    
    def __init__(self, name, resource_type, pool_size, max_chars):
        self.name = name
        self.max_chars = max_chars
        self.rpool = ResourcePool(resource_type, pool_size, True)
        self.characters = []
        
    def __str__(self):
        loc_string = f'{self.name} ' + str(self.rpool)
        for c in self.characters:
            loc_string += str(c)
        return loc_string
    
    def __repr__(self):
        return self.__str__()    
    
    def add_die(self, die):
        if self.rpool.capacity() <= 0:
            raise Exception('Adding die to location with max resource dice.')
        self.rpool.add(die)
        
    def capacity(self):
        return self.rpool.capacity()        
    
    # Returns an encoding for a location that can be returned for Open AI Gym
    # The encoding is an integer for the resource type (0-4), along with an
    # integer for each die on the location (1-6) up to capacity, followed
    # by encodings for each character in the game,
    def encode(self):
        obs = self.rpool.encode()
        cs = len(self.characters)
        for i in range(cs):
            obs += self.characters[i].encode()
        for i in range(self.max_chars - cs):
            obs.append(0)
        return obs    
        
    def resource_total(self):
        total = 0
        for resource in self.rpool:
            total += resource.value
        return total        
        
    # If possible, trade out the lowest valued die less than the proposed die.
    def trade_die(self, die):
        lowest_die = self.rpool.lowest_die()
        if lowest_die:
            if lowest_die.value < die.value:
                self.rpool.remove(lowest_die)
                self.rpool.add(die)
                return lowest_die
        return None
            
if __name__ == "__main__":
    
    size = random.randint(1, 5)
    loc = Location('Dreadmire', Resource.FOOD, size, 1)
    for i in range(size):
        loc.add_die(ResourceDie(Resource.FOOD))
    print(loc)
    print(loc.encode())
    
    die = ResourceDie(Resource.FOOD)
    td = loc.trade_die(die)
    print()
    print(die, 'traded for', td)