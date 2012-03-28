# -*- encoding: utf-8 -*-
import curses
from menugui.string import String
from menugui.ui.widgets.base import Widget
from menugui.colors import COLORS

class Button(Widget):
    color = {
        'normal' : 'normal',
        'active' : 'highlited',
    }
    
    def __init__(self, parent, pos_y, pos_x, label, width, fun = None):
        super(Button, self).__init__(parent, pos_y, pos_x)
        
        self._label = String(label)
        self._width = width
        self._fun = fun
    
    def refresh(self):
        c_window = self._parent._c_window
        
        c_window.addstr(self._pos_y, self._pos_x, self._label.center(self._width), self.flags() )
        
    def flags(self):
        if self._highlited:
            name = self.color['active']
            flags = COLORS[name]
        else:
            name = self.color['normal']
            flags = COLORS[name]
            
        if self._active:
            flags |= curses.A_BOLD
        
        return flags

    def _on_char(self, var):
        if var[0] == 10:
            self.runme()
        else:
            return var

    def runme(self):
        if self._fun != None:
            self._fun()
    
    @property
    def width(self):
        return self._width

    def set_label(self, label):
        self._label = String(label)
    
