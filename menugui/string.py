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
    
    def __str__(self):
        return self.onscreen
    
    def __unicode__(self):
        return self._text

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
    
    def put(self, data, where = None):
        data = forceUnicode(data)
        if where == None:
            self._text = self._text + data
        else:
            self._text = self._text[:where] + data + self._text[where:]
    
    def throw(self, where):
        if where == 0:
            self._text = self._text[1:]
        else:
            self._text = self._text[:where-1] + self._text[where:]

def forceUnicode(text):
    if type(text) == unicode:
        return text
    elif type(text) == str:
        return text.decode('utf8')
    else:
        return unicode(text)
