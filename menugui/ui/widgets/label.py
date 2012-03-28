# -*- encoding: utf-8 -*-
import curses
from menugui.string import String
from menugui.ui.widgets.base import Widget

class Label(Widget):
    
    def __init__(self, parent, pos_y, pos_x, label):
        super(Label, self).__init__(parent, pos_y, pos_x)
        self._label = String(label)
    
    def refresh(self):
        c_window = self._parent._c_window
        
        c_window.addstr(self._pos_y, self._pos_x, self._label.onscreen, self.flags())
    
    def flags(self):
        if self._active:
            flags = curses.A_BOLD
        else:
            flags = 0
        
        return flags

    @property
    def width(self):
        return len(self._label)
