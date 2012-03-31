# -*- encoding: utf-8 -*-
import curses
from menugui.string import String
from menugui.ui.widgets.base import Widget
from copy import copy
from menugui.validators import AllMask, Mask

class TextLine(Widget):
    
    def __init__(self, parent, pos_y, pos_x, width, input_mask=AllMask()):
        super(TextLine, self).__init__(parent, pos_y, pos_x)
        self._width = width
        
        self._first_character = 0
        self._cursor_character = 0
        
        self._data = String('')
        self._active = False
        self._running = False
        self._input_mask = input_mask
    
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
        if text_length == 0:
            c_window.addstr(self._pos_y, self._pos_x, ' ', flags)
        else:
            c_window.addstr(self._pos_y, self._pos_x, data +' ', flags)
        
        pos_x = self._pos_x + self._cursor_character - self._first_character
        c_window.move(self._pos_y, pos_x)
    
    @property
    def width(self):
        return self._width
    
    @property
    def data(self):
        try:
            return self._input_mask(self._data)
        except Mask.MaskError:
            return ''
    
    @property
    def data_width(self):
        return len(self._data)

    @data.setter
    def data(self, data):
        self._data = String(data)
        self.end()
    
    def cursor_right(self):
        self._cursor_character += 1
        if self._cursor_character > self.data_width:
            self._cursor_character = self.data_width
        if self._cursor_character - self._first_character > (self.width - 1):
            self._first_character = self._cursor_character - self.width + 1
        
        if self._first_character == self._cursor_character - self.width -2:
            self._first_character = self._cursor_character - self.width + 5
    
    def cursor_left(self):
        self._cursor_character -= 1
        if self._cursor_character < 0:
            self._cursor_character = 0
        if self._cursor_character < self._first_character:
            self._first_character = self._cursor_character
        
        if self._cursor_character == self._first_character and self._first_character != 0:
            self._first_character = self._cursor_character - 1
    
    def home(self):
        self._cursor_character = 0
        self._first_character = 0
    
    def end(self):
        self._cursor_character = self.data_width
        self._first_character = self._cursor_character - self.width + 1
        if self._first_character < 0:
            self._first_character = 0
    
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
            return var
        elif var[0] == 27: #ESC
            self._running = False
            return var
        elif var[0] == 263 or var[0] == 127:
            self.backspace()
        elif var[0] == 260: # cursor left
            self.cursor_left()
        elif var[0] == 261: # cursor right
            self.cursor_right()
        elif var[0] == 262: # home
            self.home()
        elif var[0] == 360: # end
            self.end()
        elif var[0] == 330: # delete
            self.delete()
        elif var[0] == 9: # tab character
            return var
        else:
            try:
                data = chr(var[0])
                if var[1] != None and var[1] != -1:
                    data += chr(var[1])
                
                new_data = copy(self._data)
                new_data.put(data, self._cursor_character)
                try:
                    self._input_mask(new_data)
                    self._data.put(data, self._cursor_character)
                    self.cursor_right()
                except Mask.MaskError:
                    pass
            except ValueError:
                #return unknow character
                return var
        
    def _on_get_focus(self):
        curses.curs_set(1)
    
    def _on_lost_focus(self):
        curses.curs_set(0)
