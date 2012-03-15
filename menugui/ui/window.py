# -*- encoding: utf-8 -*-
import curses
import sys
from menugui.string import String
from menugui.settings import SETTINGS

class Window(object):
    
    class WindowTitle(object):
        def __init__(self, text, parent):
            self._text = String(text)
            self._parent = parent
        
        def refresh(self, flags):
            center = ((self._parent.width-2)/2)-(len(self)/2)+1
            self._parent._c_window.addstr(0, center, self._text.onscreen, flags)
            
        def __len__(self):
            return len(self._text)
    #---------------------------------------------------------------------------
    
    def __init__(self, title, parent = None, pos_x = None, pos_y = None, width = None, height = None):
        def setX():
            if pos_x == None:
                if parent == None:
                    self._pos_x = 0
                else:
                    self._pos_x = parent._pushed_x
            else:
                self._pos_x = pos_x
                
        def setY():
            if pos_y == None:
                if parent == None:
                    self._pos_y = 0
                else:
                    self._pos_y = parent._pushed_y
            else:
                self._pos_y = pos_y
        #-----------------------------------------------------------------------
        self._title = self.WindowTitle(title, self)
        self._parent = parent
        
        setX()
        setY()
        
        self._width = width
        self._height = height
        
        self._c_window = None
        self._active = False
    
    def _new_window(self):
        if self._c_window != None:
            self._c_window.erase()
        self._c_window = curses.newwin(self.height, self.width, self.pos_y, self.pos_x)
    
    @property
    def _pushed_x(self):
        return self._pos_x + SETTINGS['push_x']
    
    @property
    def _pushed_y(self):
        return self._pos_y + SETTINGS['push_y']
    
    @property
    def pos_x(self):
        return self._pos_x
    
    @property
    def pos_y(self):
        return self._pos_y
    
    @property
    def height(self):
        if self._height == None:
            return 3
        else:
            return self._height
    
    @property
    def width(self):
        if self._width == None:
            return len(self._title) + 2
        else:
            return self._width

    def refresh(self):
        if self._active:
            flags = curses.A_BOLD
        else:
            flags = 0
            
        data = self._generate_data()
        self._new_window()
        self._c_window.border()
        self._title.refresh(flags)
        
        loop = 0
        for line in data:
            loop += 1
            self._c_window.addstr(loop, 1, line[0], line[1]|flags)

        self._c_window.refresh()
    
    def _generate_data(self):
        pass
    
    def setActive(self, active):
        self._active = active
