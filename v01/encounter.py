# -*- coding: utf-8 -*-
"""
Game encounter deck.
"""

from deck import Deck

class EncounterDeck(Deck):
    
    NONTIMER = 0
    TIMER = 1
    
    def __init__(self, timers, non_timers):
        self.cards = [EncounterDeck.TIMER for i in range(timers)]
        self.cards.extend([EncounterDeck.NONTIMER for i in range(non_timers)])
        super().__init__(self.cards)
        
if __name__ == "__main__":
    
    ed = EncounterDeck(6, 10)  
    print(ed.draw())