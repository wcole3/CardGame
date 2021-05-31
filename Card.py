#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:25:40 2020

Class representing a card object.

A card should have suite and value

@author: wcole
"""

class Card:
    
    def __init__(self, values : list, suite : str, name : str):
        '''
        Construct a card object

        Parameters
        ----------
        value : list
            The possible values of the card.
        suite : str
            The suite of the card.
        name : str
            The name of the card.  Does not include suite.

        Returns
        -------
        None.

        '''
        self.values = values
        self.suite = suite
        self.name = name
        self.fullName = self.name + " of " + self.suite
    
    
    def getValues(self):
        try:
            self.values = sorted(self.values, key=int, reverse=True)
        except AttributeError:
            return self.values
        return self.values
    
    def getSuite(self):
        return self.suite
    
    def getName(self):
        return self.name
    
    def getFullName(self):
        return self.fullName

