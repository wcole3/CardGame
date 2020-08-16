#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:41:27 2020

Class for a deck object.  A deck contains enough cards to have one version
of each name suite combo defined in input xml.

@author: wcole
"""

import Card
import CardGameUtils as util


class Deck:
    
    def __init__(self, xmlFile):
        try:
            self.cards = util.getCardsFromFile(xmlFile)
        except Exception:
            print("Error loading deck")
            
        
    
