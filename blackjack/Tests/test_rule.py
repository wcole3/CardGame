# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 15:38:45 2021

Test case for Rule class

@author: William_Cole
"""
import sys
sys.path.insert(0,'..')#hack it
import unittest
import CardGameUtils as utils
import GameConstants as gc
from Deck import Deck
from Card import Card
import Rule
from Strategy import Strategy

class testRule(unittest.TestCase):
    
    def testDealerRuleParse(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        strat = Strategy("../../Strategies/DealerStrategy.xml")
        self.assertEqual(len(strat.rules), 1)
        rule = strat.rules[0]
        self.assertEqual(rule.true_action, "HIT")
        self.assertEqual(rule.false_action, "STAND")
        logic = rule.ruleStatements
        self.assertEqual(len(logic), 4)
        self.assertEqual(logic[0], Rule.LOGIC_IF)
        self.assertEqual(logic[1], Rule.VAR_Score)
        self.assertEqual(logic[2], 'lt')
        self.assertEqual(int(logic[3]), 17)
        '''
        hand =[deck.getCard("Clubs", "Six"), deck.getCard("Diamonds", "Queen")]
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.HIT)
        self.assertEqual(strat.getScore(), 16)
        hand.append(deck.getCard("Spades", "Two"))
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.STAND)
        self.assertEqual(strat.getScore(), 18)
        hand.append(deck.getCard("Hearts", "King"))
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.BUST)
        self.assertEqual(strat.getScore(), 0)
        '''
        
        
if __name__ == "__main__":
    unittest.main()