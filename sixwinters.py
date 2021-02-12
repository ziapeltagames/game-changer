# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:52:26 2020

@author: phill
"""

import random

from character import Skill, Character
from location import Location
from resource import Resource, ResourcePool

from character_deck import CharacterDeck
from encounter import EncounterDeck
from achievement import AchievementDeck, AchievementType, TotalResourceAchievement

MAX_TIMERS = 5
RESOURCE_POOL_SIZE = 3
LOCATION_POOL_SIZE = 2

# Initialize characters and locations
locations = [Location('Dreadmire', Resource.ORE, LOCATION_POOL_SIZE),
             Location('Monkeytown', Resource.TIMBER, LOCATION_POOL_SIZE),
             Location('Flavortown', Resource.FOOD, LOCATION_POOL_SIZE),
             Location('Taos', Resource.MANA, LOCATION_POOL_SIZE)]

characters = [Character('Keel'), Character('Thea')]

character_deck = CharacterDeck()
encounter_deck = EncounterDeck(6, 10)
achievement_deck = AchievementDeck()

# Initialize resource pools
resource_pools = []
for resource in Resource:
    resource_pools.append(ResourcePool(resource, RESOURCE_POOL_SIZE))

# Initialize timers seen so far
total_timers = 0

# Initialize where characters are located
for character in characters:
    character.location = locations[0]
    locations[0].characters.append(character)
    
# Create initial achievements
ach1 = TotalResourceAchievement('Gather Wood', AchievementType.RESOURCE, 
                                Resource.TIMBER, 5)
ach2 = TotalResourceAchievement('Gather Mana', AchievementType.RESOURCE, 
                                Resource.MANA, 7)
achievements = [ach1, ach2]
    
# Randomly shuffles a character from one location to another
def randomly_move_characters(character):
    character.location.characters.remove(character)
    new_location = random.randint(0, len(locations) - 1)
    character.location = locations[new_location]
    character.location.characters.append(character)
    
# A simple heuristic for investing resources from the pool to the location
def greedy_invest_resources(location):

    # Iterate over each location that has characters
    if len(location.characters) <=0:
        return
    
    skill_total = 0
        
    for character in location.characters:
        skill_total += character.skills[Skill.COMMAND]
    
    # What's the largest die that can be taken
    pool = resource_pools[location.rpool.resource_type.value]
    die = pool.highest_die_under(skill_total)
    
    # Can't get anything
    if die == None:
        return
    
    # Does the location have space available, if so, fill it
    if location.capacity() > 0:
        location.add_die(die)
        pool.remove(die)
        return
        
    # Otherwise, attempt to swap it out
    swapped_die = location.trade_die(die)        
    if swapped_die == None:
        return
    
    pool.remove(die)
    pool.add(swapped_die)

        
# Iterate for some number of timers
while total_timers < MAX_TIMERS:
    
    # Refill the resource pools
    for resource_pool in resource_pools:
        resource_pool.refill()
    
    # Move characters, randomly for now
    for character in characters:
        randomly_move_characters(character)
    
    # Invest resources using a greedy heuristic
    for location in locations:
        greedy_invest_resources(location)
    
    # Check to see if any achievements have been completed
    for achievement in achievements:
        if achievement.completed(locations):
            print('Completed!', achievement)
        
    total_timers+= 1

print('End Game State')
for location in locations:
    print(location)