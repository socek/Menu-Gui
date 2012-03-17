# -*- encoding: utf-8 -*-
from menugui.string import forceUnicode, String
from menugui.colors import COLORS

class BaseElement(object):
    color = {
        'normal' : 'normal',
        'active' : 'highlited',
    }
    
    def __init__(self, name, data):
        self._name = forceUnicode(name)
        self._data = data
        self._parent = None
        self._type = None
    
    def _set_parent(self, parent, type):
        self._parent = parent
        self._type = type
    
    @property
    def name(self):
        return self._name

    def flags(self, state):
        name = self.color[state]
        return COLORS[name]

class MenuElement(BaseElement):
    
    def run(self):
        if self._data == None:
            pass
        else:
            self._data(self._parent)

class ListElement(BaseElement):

    def run(self):
        return self._data
    
    
