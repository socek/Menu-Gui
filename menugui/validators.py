# -*- encoding: utf-8 -*-
import re

class Validator(object):
    regexp = None
    
    def __init__(self):
        if self.regexp != None:
            self._regexp = re.compile(self.regexp)
    
    def validate(self, text):
        if self._regexp.match(text._text) == None:
            return False
        else:
            return True

class AllValidator(Validator):
    def validate(self, text):
        return True

class IntValidator(Validator):
    regexp = r'^[0-9]+$'
