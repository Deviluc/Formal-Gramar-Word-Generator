#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 17:49:22 2017

@author: bugs
"""
import re

class Rule:
    
    def __init__(self, string):
        self.var = string[0:string.find("->")].strip()
        self.replacements = []
        
        start_index = string.find("->") + 2
        end_index = start_index
        
        string.replace
        
        while end_index is not len(string) and start_index <= len(string):
            end_index = string.find("|", start_index)
            end_index = end_index if end_index is not -1 else len(string)
            
            self.replacements.append(string[start_index:end_index].strip())
            start_index = end_index + 1
    
    def __str__(self):
        return self.var + " -> " + "|".join(self.replacements)
    
    def is_applicable(self, string):
        return string.find("'" + self.var + "'") is not -1
    
    def apply_first(self, string):
        return [string.replace("'" + self.var + "'", repl, 1) for repl in self.replacements]
        

class WordGenerator:
    
    def __init__(self, rules):
        self.rules = rules
        
    def generate_words(self, max_length):
        
        def str_len_no_vars(string):
            tmp_str = string
            for match in re.findall("'[^']+?'", string):
                tmp_str = tmp_str.replace(match, "")
            return len(tmp_str)
        
        words = set(["'S'"])
        may_replace = True
        max_len_reached = False
        
        while may_replace and not max_len_reached:
            new_words = set()
            may_replace = False
            max_len_reached = True
            for word in words:
                if str_len_no_vars(word) <= max_length:
                    max_len_reached = False
                    was_applied = False
                    for rule in self.rules:
                        if rule.is_applicable(word):
                            may_replace = True
                            was_applied = True
                            for gen_word in rule.apply_first(word):
                                new_words.add(gen_word)
                    if not was_applied:
                        new_words.add(word)
                    
            words = new_words
        
        return [word for word in words if word.find("'") is -1]
        #return words
    
rules = [Rule("S -> 0'B'|1'A'"), Rule("A -> 0|0'S'|1'A''A'"), Rule("B -> 1|1'S'|0'B''B'")]
g = WordGenerator(rules)
words = g.generate_words(8)
print(words)
