# -*- encoding: utf-8 -*-
from log import LOGGER

class String(object):
    def __init__(self, text):
        if type(text) == unicode:
            self._text = text
        else:
            self._text = text.decode('utf8')
    
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
