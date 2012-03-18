# -*- encoding: utf-8 -*-
from log import LOGGER

class String(object):
    def __init__(self, text):
        self._text = forceUnicode(text)
    
    @property
    def onscreen(self):
        return self._text.encode(LOGGER.getLocale())
    
    @property
    def value(self):
        return self._text
    
    def __len__(self):
        return len(self._text)

    def center(self, num):
        return self._text.center(num).encode(LOGGER.getLocale())
    
    def full(self, num):
        length = len(self._text)
        text = self._text + (' '*(num-length))
        return text.encode(LOGGER.getLocale())
    
    def part(self, start=0, end = None):
        if end == None:
            text = self._text[start:]
        else:
            text = self._text[start:end]
        return text.encode(LOGGER.getLocale())

def forceUnicode(text):
    if type(text) == unicode:
        return text
    else:
        return text.decode('utf8')
