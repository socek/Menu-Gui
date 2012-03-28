# -*- encoding: utf-8 -*-
import curses
from time import sleep

class Widget(object):
    
    def __init__(self, parent, pos_y, pos_x):
        self._parent = parent
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._active = False
        self._highlited = False

    def _on_get_focus(self):
        pass

    def _on_lost_focus(self):
        pass
    
    def processed_character(self):
        c_window = self._parent._c_window
        self.refresh()
        c_window.refresh()
        char = self.getch()
        return self._on_char(char)

    def run(self):
        self._on_get_focus()
        while self._running:
            self.processed_character()
        self._on_lost_focus()
    
    def getch(self):
        c_window = self._parent._c_window
        c_window.keypad(1)
        c_window.timeout(0)
        
        char = c_window.getch()
        char2 = None
        while char == -1:
            sleep(0.01)
            char = c_window.getch()
            
        if char == 27 or char > 127:
            char2 = c_window.getch()
                
        return (char, char2)
    
    def set_active(self, value):
        self._active = value
    
    def set_highlited(self, value):
        self._highlited = value
    
    @property
    def width(self):
        return 0
