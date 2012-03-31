# -*- encoding: utf-8 -*-
import re
from menugui.string import String

class Mask(object):
    class MaskError(Exception): pass
    regexp = None
    
    def __init__(self):
        if self.regexp != None:
            self._regexp = re.compile(self.regexp)
    
    def __call__(self, text):
        if self._regexp.match(text._text) == None:
            return text
        else:
            raise self.MaskError()

class AllMask(Mask):
    def __call__(self, text):
        return text

class IntMask(Mask):
    def __call__(self, text):
        try:
            if type(text) == String:
                return int(text._text)
            else:
                return int(text)
        except ValueError:
            raise self.MaskError()

