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
            self.true_action = root_element.get(ATTR_TrueAction)
            self.false_action = root_element.get(ATTR_FalseAction)
            self.ruleStatements = self.parseLogic(root_element.find("Logic"))
            if(DEBUG): print(self.ruleStatements)
        else:
            raise ValueError("Rule cannot be constructed from None-type object")
            
    def parseLogic(self, element):
        #figure out which logic operation
        attrs = []
        op = element.get(ATTR_operation)
        if op == LOGIC_IF:
            #working logic
            var = element.get(ATTR_variable)
            check = element.get(ATTR_check)
            value = element.get(ATTR_value)
            attrs = [LOGIC_IF, var, check, value]
        elif op == LOGIC_AND:
            attrs = [LOGIC_AND]
            children = []
            for logic in element.findall("Logic"):
                children.append(self.parseLogic(logic))
            attrs.append(children)
        elif op == LOGIC_OR:
            attrs = [LOGIC_OR]
            children = []
            for logic in element.findall("Logic"):
                children.append(self.parseLogic(logic))
            attrs.append(children)
        elif op == LOGIC_NOT:
            attrs = [LOGIC_NOT, self.parseLogic(element.find("Logic"))]
        return attrs
    
    def evaluate(self):
        return self.evaluateRule(self.ruleStatements)
    
    def evaluateRule(self, rules):
        #evaluate the rule and return the true or false action
        if len(rules) != 0:
            op = rules[0]
            if op == LOGIC_IF:
                return self.evaluateIF(rules)
            elif op == LOGIC_AND:
                print('and')
            elif op == LOGIC_OR:
                print('or')
            elif op == LOGIC_NOT:
                print('Not')
        else:
            raise ValueError("No rule statements found for rule")
            
    def evaluateIF(self, logic):
        print("eval_if")
        
        
            
