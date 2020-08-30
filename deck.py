# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:16:54 2020

@author: phill
"""

from random import shuffle

class Deck:
    
    def __init__(self, cards):
        self.cards = cards
        shuffle(self.cards)

    # Pull a card from the deck
    def draw(self):
        return self.cards.pop(0)
    
    def reshuffle(self):
        shuffle(self.cards)