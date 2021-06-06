# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 16:53:37 2021

Object repr of rule from xml file

@author: Wellb_000
"""

import xml.etree.ElementTree as ET
import GameConstants as gc

DEBUG = gc.DEBUG

ATTR_TrueAction = "true_action"
ATTR_FalseAction = "false_action"
ATTR_operation = "operation"
ATTR_variable = "var"
ATTR_check = "check"
ATTR_value = "value"

LOGIC_IF = "IF"
LOGIC_AND = "AND"
LOGIC_OR = "OR"
LOGIC_NOT = "NOT"

VAR_Score = "SCORE"
VAR_DealerShown = "DEALERSHOWN"
VAR_KNOWNCOUNT = "COUNT"

class Rule:
    
    def __init__(self, root_element):
        if root_element is not None:
            self.logicStatements = []
            self.true_action = root_element.get(ATTR_TrueAction)
            self.false_action = root_element.get(ATTR_FalseAction)
            for logic in root_element:
                self.logicStatements.append(self.parseLogic(logic))
        else:
            raise ValueError("Rule cannot be constructed from None-type object")
            
    def parseLogic(self, logicElement):
        #figure out which logic operation
        op = logicElement.get(ATTR_operation)
        if op == LOGIC_IF:
            print("IF")
        elif op == LOGIC_AND:
            print("AND")
        elif op == LOGIC_OR:
            print("OR")
        elif op == LOGIC_NOT:
            print("NOT")
