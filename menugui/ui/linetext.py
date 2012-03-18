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
    
    def set_data(self, data):
        self._data = String(data)
    
    def set_active(self, active):
        self._active = active

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
        c_window.addstr(self._pos_y, self._pos_x, data, flags)

    @property
    def width(self):
        return self._width
    
    @property
    def data(self):
        return self._data

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
            self.validator(char)
            
        curses.curs_set(0)
    
    def getch(self):
        c_window = self._parent._c_window
        c_window.keypad(1)
        c_window.timeout(0)
        
        char = c_window.getch()
        while char == -1:
            sleep(0.01)
            char = c_window.getch()
            if char == 27:
                char2 = c_window.getch()
                if char2 != -1:
                    char = char2
            elif char > 127:
                char2 = c_window.getch()
                char = (char, char2)
        return char
    
    def validator(self, var):
        #raise RuntimeError( var )
        #print var
        print 'valid:', var
        if var == 10:
            self._running = False
            return False
        elif var == 27:
            print 'e:', var
            print 'b:', self._parent._c_window.getch()
        
        return True
        if 1 : pass
        elif var == 263 or var == 127:
            #self.backspace()
            return False
        elif var == 260: # kursor w lewo
            #self.cursor_left()
            return False
        elif var == 261: # kursor w prawo
            #self.cursor_right()
            return False
        elif var == 262: # home
            #self.cursor_home()
            return False
        elif var == 360:
            #self.cursor_end()
            return False
        elif var == 274:
            self._running = False
            self.text = None
            return False
        elif var > 250 or var < 0:
            return False
            #raise RuntimeError( var )

        #Tutaj dojdzie, jeśli nie było żadnej innej akcji
        if self._cursor >= self.text_length():
            self.text += chr( var )
        else:
            listtext = list( self.text )
            listtext[ self._cursor ] = chr( var )
            self.text = ''.join( listtext )
        self.cursor_right()
        return True
