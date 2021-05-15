# -*- coding: utf-8 -*-
"""
Deck of character cards for chance resolution.
"""

from deck import Deck

class CharacterDeck(Deck):
    
    def __init__(self):
        self.cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        super().__init__(self.cards)
        
if __name__ == "__main__":
    
    ad = CharacterDeck()  
    print(ad.draw())