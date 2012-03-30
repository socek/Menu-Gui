# -*- encoding: utf-8 -*-
import curses
import sys
from menugui.string import String
from menugui.settings import SETTINGS
from menugui.colors import COLORS

class Window(object):
    
    class WindowTitle(object):
        def __init__(self, text, parent):
            self._text = String(text)
            self._parent = parent
        
        def set_title(self, text):
            self._text = String(text)
        
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
        self._data = []
    
    def _new_window(self):
        if self._c_window != None:
            self._c_window.erase()
            self._c_window.refresh()
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
            return len(self._data) + 2
        else:
            return self._height
    
    @property
    def width(self):
        if self._width == None:
            elements_width = len(self._title)
            number_of_elements = len(self._data)
            for line in self._data:
                elements_width = (elements_width >= len(line[0]) ) and elements_width or len(line[0])
            return elements_width + 2
        else:
            return self._width

    def refresh(self, window_refresh=True):
        if self._active:
            flags = curses.A_BOLD
        else:
            flags = 0
            
        data = self._generate_data()
        self._new_window()
        self._c_window.border()
        self._title.refresh(flags)
        
        loop = 0
        if data != None:
            for line in data:
                loop += 1
                self._c_window.addstr(loop, 1, String(line[0]).center(self.width-2), line[1]|flags)

        if window_refresh:
            self._c_window.refresh()
    
    def _generate_data(self):
        return self._data
    
    def set_data(self, data):
        self._data = data
    
    def set_active(self, active):
        self._active = active

    def close(self):
        self._c_window.erase()
        self._c_window.refresh()
        if self._parent != None:
            self._parent.set_active(True)
            self._parent.refresh()

    def __call__(self, menu):
        self.run()
        
    def set_window_title(self, title):
        self._title.set_title(title)
