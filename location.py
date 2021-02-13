# -*- coding: utf-8 -*-
"""
Locations have a name, resource types, and a maximum number of resource dice
they can hold.

Created on Sun Aug 30 09:07:53 2020

@author: phill
"""

import random
from resource import Resource, ResourceDie, ResourcePool

# TODO: Add the ability to handle multiple resource types.
class Location:
    
    def __init__(self, name, resource_type, pool_size):
        self.name = name
        self.rpool = ResourcePool(resource_type, pool_size, True)
        self.characters = []
        
    def __str__(self):
        loc_string = f'{self.name} {self.rpool.pool_size} '
        for r in self.rpool:
            loc_string += str(r) + ' '
        return loc_string
    
    def __repr__(self):
        return self.__str__()    
        
    def resource_total(self):
        total = 0
        for resource in self.rpool:
            total += resource.value
        return total
    
    def capacity(self):
        return self.rpool.capacity()
    
    def add_die(self, die):
        if self.rpool.capacity() <= 0:
            raise Exception('Adding die to location with max resource dice.')
        self.rpool.add(die)
        
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
    
    size = random.randint(1, 6)
    loc = Location('Dreadmire', Resource.FOOD, size)
    for i in range(size):
        loc.add_die(ResourceDie(Resource.FOOD))
    print(loc)

    die = ResourceDie(Resource.FOOD)
    td = loc.trade_die(die)
    print()
    print(die, 'traded for', td)