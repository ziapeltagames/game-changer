# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 09:08:28 2020

@author: phill
"""

from deck import Deck

class AssetDeck(Deck):
    
    def __init__(self):
        self.cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
        super().__init__(self.cards)
        
if __name__ == "__main__":
    
    ad = AssetDeck()  
    print(ad.draw())