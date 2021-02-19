# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:52:26 2020

@author: phill
"""

import gym
from gym import spaces
from gym.utils import seeding

import random

from deck import Deck
from character import Skill, Character
from location import Location
from resource import Resource, ResourcePool
from achievement import AchievementType, SumResourceAchievement

# A simple upper bound on the length of the game
MAX_TIMERS = 5

# The number of dice in each resource pool at the start of each turn
RESOURCE_POOL_SIZE = 3

# The max number of resource dice which may be placed on each location
LOCATION_POOL_SIZE = 2
    
# Randomly shuffles a character from one location to another
def randomly_move_characters(character, locations):
    character.location.characters.remove(character)
    new_location = random.randint(0, len(locations) - 1)
    character.location = locations[new_location]
    character.location.characters.append(character)
    
# Remove dice from the listed locations
def pay_for_achievement(loc_dice):
    for ld in loc_dice:
        ld.location.rpool.remove(ld.die)
    
# A simple heuristic for investing resources from the pool to the location
def greedy_invest_resources(location, resource_pools):

    # Iterate over each location that has characters
    if len(location.characters) <= 0:
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
    
# This is the Open AI Gym environment for tracking state
class SixWinters(gym.Env):
    
    # The most important parts of the environment are the action_space
    # and the observation_space. Essentially, what the AI can see
    # and what the AI can do
    def __init__(self):
        
        # Each character may move to a different location
        self.action_space = spaces.Tuple((
            spaces.Discrete(4),
            spaces.Discrete(4)))
        
        # The board state is represented as 60 discrete values
        obs = []
        for i in range(60):
            obs.append(6)
            
        self.observation_space = spaces.MultiDiscrete(obs)        
        self.seed()
        self.reset()
        
    # Bookkeeping to move a character from one location to another
    def _move_character(self, character, location):
        
        # Remove current character from list of characters at location
        character.location.characters.remove(character)
        
        # Update character reference and location reference
        character.location = location
        location.characters.append(character)
        
    # Returns game state, called at the end of each step
    def _get_obs(self):
        
        obs = []
        
        for loc in self.locations:
            obs.extend(loc.encode())
            
        for rp in self.resource_pools:
            obs.extend(rp.encode())
            
        for achievement in self.current_achievements:
            obs.extend(achievement.encode())
        
        # 0 pad out missing achievements
        for i in range(2 - len(self.current_achievements)):
            obs.extend([0, 0, 0])
        
        return obs
        
    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]        
        
    # This advances the state of the world one step, by passing in the
    # action the AI takes.
    def step(self, action):
        
        # Make sure this is a valid action
        assert self.action_space.contains(action)
        
        for resource_pool in self.resource_pools:
            resource_pool.refill()
            
        # Move characters based on actions        
        self._move_character(self.characters[0], self.locations[action[0]])
        self._move_character(self.characters[1], self.locations[action[1]])
        
        # Invest resources based on greedy heuristic
        for location in self.locations:
            greedy_invest_resources(location, self.resource_pools)
            
        # Check to see if achievements have been completed
        # Create a duplicate list so the original can be modified during iteration
        for achievement in list(self.current_achievements):            
            subset = achievement.completed(self.locations)            
            if subset:
                pay_for_achievement(subset[0])
                
                self.current_achievements.remove(achievement)
                self.score = self.score + 1
                
                new_achievement = self.achievement_deck.draw()

                if new_achievement is not None:
                    self.current_achievements.append(new_achievement)
                    
                # All of the achievments are completed!
                if not self.current_achievements:
                    self.done = True
        
        # For now, the game lasts a fixed number of rounds
        self.timers = self.timers + 1
        
        if self.timers >= MAX_TIMERS:
            self.done = True
            
        return self._get_obs(), self.score, self.done, {}
        
        
    # Reset the state of the game world
    def reset(self):

        # Initialize characters and locations
        self.locations = [Location('Ore Town', Resource.ORE, LOCATION_POOL_SIZE),
                          Location('Timberville', Resource.TIMBER, LOCATION_POOL_SIZE),
                          Location('Flavortown', Resource.FOOD, LOCATION_POOL_SIZE),
                          Location('Manasberg', Resource.MANA, LOCATION_POOL_SIZE)]
        
        self.characters = [Character('Keel'), Character('Thea')]
        
        # Make a deck of achievements
        self.achievement_deck = Deck([])
        
        # Initialize resource pools
        self.resource_pools = []
        for resource in Resource:
            self.resource_pools.append(ResourcePool(resource, RESOURCE_POOL_SIZE))
        
        # Initialize where characters are located
        for character in self.characters:
            character.location = self.locations[0]
            self.locations[0].characters.append(character)
            
        # Create initial four achievements, which map to the four location types
        for next_resource in [Resource.TIMBER, Resource.MANA, Resource.ORE, Resource.FOOD]:
            
            achievement = SumResourceAchievement('Gather', AchievementType.SUM, next_resource, 7)
            self.achievement_deck.insert(achievement)

        # Draw two starting achievements           
        self.achievement_deck.shuffle()
        self.current_achievements = [self.achievement_deck.draw(),
                                     self.achievement_deck.draw()]
        
        self.done = False
        self.timers = 0
        self.score = 0
        
if __name__ == "__main__":
    
    # A random strategy to exercise the gym.Env
    env = SixWinters()
    done = False
    r = 0
    while not done:
        action = (random.randint(0,3), random.randint(0,3))
        obs, r, done, info = env.step(action)
    
    print('Done playing, score', r)