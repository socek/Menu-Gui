# -*- encoding: utf-8 -*-
import curses
ESCAPES = [ '\xc5', '\xc4', '\xc3' ]
from menugui.string import String
from time import sleep

class TextLine(object):
    
    def __init__(self, parent, pos_y, pos_x, width):
        self._parent = parent
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._width = width
        
        self._first_character = 0
        self._cursor_character = 0
        
        self._data = None
        self._active = False
        self._running = False
    
    def refresh(self, flags = 0):
        c_window = self._parent._c_window
        if self._active:
            flags |= curses.A_BOLD
        
        text_length = len(self._data)
        visible_text_length = self.width - 1
        
        start = self._first_character
        end = self._first_character + visible_text_length
        data = self._data.part(start, end)
        
        c_window.addstr(self._pos_y, self._pos_x, ' '*visible_text_length, flags)
        c_window.addstr(self._pos_y, self._pos_x, data +' ', flags)
        
        pos_x = self._pos_x + self._cursor_character - self._first_character
        c_window.move(self._pos_y, pos_x)
    
    def set_active(self, active):
        self._active = active

    @property
    def width(self):
        return self._width
    
    @property
    def data(self):
        return self._data
    
    @property
    def data_width(self):
        return len(self._data)

    @data.setter
    def data(self, data):
        self._data = String(data)

    def run(self):
        curses.curs_set(1)
        c_window = self._parent._c_window
        self._running = True
        while self._running:
            self.refresh()
            c_window.refresh()
            
            char = self.getch()
            self._on_char(char)
            
        curses.curs_set(0)
    
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
    
    def cursor_right(self):
        self._cursor_character += 1
        if self._cursor_character > self.data_width:
            self._cursor_character = self.data_width
        if self._cursor_character - self._first_character > (self.width - 1):
            self._first_character = self._cursor_character - self.width + 1
    
    def cursor_left(self):
        self._cursor_character -= 1
        if self._cursor_character < 0:
            self._cursor_character = 0
        if self._cursor_character < self._first_character:
            self._first_character = self._cursor_character
    
    def home(self):
        self._cursor_character = 0
        self._first_character = 0
    
    def end(self):
        self._cursor_character = self.data_width
        self._first_character = self._cursor_character - self.width + 1
    
    def backspace(self):
        if self._cursor_character == 0:
            return
        self._data.throw(self._cursor_character)
        self.cursor_left()
    
    def delete(self):
        self._data.throw(self._cursor_character+1)
    
    def _on_char(self, var):
        if var[0] == 10:
            self._running = False
            return False
        elif var[0] == 27 and var[1] == -1: #ESC
            self._running = False
            return False
        elif var[0] == 263 or var[0] == 127:
            self.backspace()
            return False
        elif var[0] == 260: # cursor left
            self.cursor_left()
            return False
        elif var[0] == 261: # cursor right
            self.cursor_right()
            return False
        elif var[0] == 262: # home
            self.home()
            return False
        elif var[0] == 360: # end
            self.end()
            return False
        elif var[0] == 330: # delete
            self.delete()
            return False
        else:
            try:
                data = chr(var[0])
                if var[1] != None and var[1] != -1:
                    data += chr(var[1])
                    
                self._data.put(data, self._cursor_character)
                self.cursor_right()
                return True
            except ValueError:
                #do nothing if unknow character accured
                #print var
                pass
