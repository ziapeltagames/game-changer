# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:07:53 2020

@author: phill
"""

from resource import Resource, ResourceDie, ResourcePool

# TODO: Make a fixed sized list of resource dice, with "zero" dice
# filling the empty slots, then could compare the first / lowest item
# on the list with the highest die from the resource pool, and then
# could make that trade

class Location:
    
    def __init__(self, name, resource_type, pool_size):
        self.name = name
        self.pool_size = pool_size
        self.resource_type = resource_type
        self.resources = [0] * pool_size
        self.characters = []
        
    def get_total(self):
        total = 0
        for resource in self.resources:
            total += resource.value
        return total
    
    # TODO - Is it easier to determine invest or trade if the dice
    # are in a sorted list? Maybe from highest to lowest?
    def add_die(self, die):
        print('TBD')
        
if __name__ == "__main__":
    
    loc = Location('Dreadmire', Resource.FOOD, 3)
    loc.add_die(ResourceDie(Resource.FOOD))
    loc.add_die(ResourceDie(Resource.FOOD))
    loc.add_die(ResourceDie(Resource.FOOD))
    print(loc.get_total())