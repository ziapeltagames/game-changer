# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:52:26 2020

@author: phill
"""

import random

from character import Character
from location import Location
from resource import Resource, ResourcePool

from character_deck import CharacterDeck
from encounter import EncounterDeck
from achievement import AchievementDeck

MAX_TIMERS = 5
POOL_SIZE = 2

locations = [Location('Dreadmire', Resource.ORE),
             Location('Monkeytown', Resource.LUXURY),
             Location('Flavortown', Resource.FOOD),
             Location('Taos', Resource.MANA)]

characters = [Character('Keel'), Character('Thea')]

character_deck = CharacterDeck()
encounter_deck = EncounterDeck(6, 10)
achievement_deck = AchievementDeck()

resource_pools = []
for resource in Resource:
    resource_pools.append(ResourcePool(resource, POOL_SIZE))

total_timers = 0

for character in characters:
    character.location = locations[0]
    character.location.characters.append(character)
    
def move_character(character):
    character.location.characters.remove(character)
    new_location = random.randint(0, len(locations) - 1)
    character.location = locations[new_location]
    character.location.characters.append(character)
    
# Determine the highest available die at or below value in resource pool
def highest_pool_die(pool, skill_total):    
    highest_die = None
 
    for die in pool.dice:        
        if die.value > skill_total:
            continue
        if highest_die == None or highest_die.value < die.value:
            highest_die = die
            
    return highest_die
    
# Move a die from a pool to a location
def invest(die, pool, location):
    
    pool.remove(die)
    location.resources.append(die)
    
# A simple heuristic for investing resources from the pool to the location
def invest_resources(location):

    # Iterate over each location that has characters
    if len(location.characters) > 0:
        skill_total = 0
        
        for character in location.characters:
            skill_total += character.command
        
        # What's the largest die that can be taken
        pool = resource_pools[location.resource_type.value]
        die = highest_pool_die(pool, skill_total)
        
        # Can't get anything
        if die == None:
            return
        
        # Does the pool have space available, if so, fill it
        if len(location.resources) < POOL_SIZE:
            invest(die, pool, location)
            return
        
        # TODO - Invest logic
        
# Iterate for some number of timers
while total_timers < MAX_TIMERS:
    
    # Refill the resource pools
    for resource_pool in resource_pools:
        resource_pool.refill()
    
    # Move characters, randomly for now
    for character in characters:
        move_character(character)
    
    # Invest resources
    for location in locations:
        
        # Move resources from the pool to a location
        invest_resources(location)
        
    total_timers+= 1