# -*- encoding: utf-8 -*-
# -- TOP IMPORTS --
import curses
from copy import copy

ESCAPES = [ '\xc5', '\xc4', '\xc3' ]

class Text(object):
    def __init__(self, y, x, title = None, text = '', only_digits = False, width = 25, autorun = True):
        self.x = x
        self.y = y
        self._title = title
        self.text = text
        self._running = True
        self._win = None
        self._cursor = 0
        self._low_cursor = 0
        self._startpost = 0
        self._width = width
        self._only_digits = only_digits
        self.cursor_end()
        if autorun:
            self.run()

    @property
    def text_width(self):
        return self._width - 3

    def run(self, clear = True):
        gflags = curses.A_BOLD

        width = self._width
        self._win = curses.newwin( 3, width, self.y, self.x)
        self._win.border()
        if self._title:
            width = self._win.getmaxyx()[1] - 2 #Nie wiem czemu musi być tak 2, ale bez tego nie działa

            center = ( width/2 ) - ( len(self._title)/2 ) + 1
            self._win.addstr( 0, center, self._title.encode( 'UTF-8' ), gflags )
        self._win.refresh()
        self._win2 = curses.newwin( 1, width, self.y+1, self.x+1)

        curses.curs_set(1)
        while self._running:
            self.refresh()
            self._win2.keypad(1)
            char = self._win2.getch()
            self.validator( char )
        curses.curs_set(0)

        if clear:
            self._win.erase()
            self._win.refresh()

    def text_length(self):
        text = copy( self.text )
        for esc in ESCAPES:
            text = text.replace( esc, '')
        return len( text )

    def refresh(self):
        width = self.text_width
        if self.text_length() < width:
            text = self.text
        else:
            text = self.text[self._startpost: self._startpost+width]
            if len( text ) < width:
                text = self.text[:width]
        self._win2.move( 0, 0 )
        self._win2.clrtoeol()
        try:
            #I don't know what is the source of the problem, so I made workaround
            #When someone use "polish" letter in front it prints something strange
            if len(text) < 2:
                text += ' '
            #end of workaround
            self._win2.addstr( 0, 0, text, curses.A_BOLD )
        except curses.error:
            raise RuntimeError( text )
        self._win2.move( 0, self._low_cursor )

    def cursor_home(self):
        self._cursor = 0
        self._low_cursor = 0
        self._startpost = 0

    def cursor_end(self):
        self._cursor = self.text_length()
        if self.text_length() > self.text_width:
            self._low_cursor = self.text_width
        else:
            self._low_cursor = self.text_length()
        self._startpost = self.text_length() - self.text_width
        if self._startpost < 0:
            self._startpost = 0

    def backspace(self):
        if self._cursor > 0:
            tmp = list( self.text )
            listtext = []
            last = []
            for char in tmp:
                if char in ESCAPES:
                    last = [char]
                else:
                    listtext.append( last + [char] )
                    last = []
            listtext.pop( self._cursor - 1 )
            self.text = ''
            for char in listtext:
                for skladowa in char:
                    self.text += skladowa
            self._cursor -= 1
            length = self.text_length()
            if length < self.text_width:
                self._low_cursor -= 1
            else:
                self._startpost -= 1

    def cursor_right(self):
        if self._cursor < self.text_length():
            self._cursor += 1
            if self._low_cursor < self.text_width:
                self._low_cursor += 1
            else:
                if self._startpost < self.text_length():
                    self._startpost += 1

    def cursor_left(self):
        if self._cursor > 0:
            self._cursor -= 1
        if self._low_cursor > 0:
            self._low_cursor -= 1
        else:
            if self._startpost > 0:
                self._startpost -= 1

    def validator(self, var):
        #raise RuntimeError( var )
        #print var
        if var == 10:
            self._running = False
            return False
        elif var == 263 or var == 127:
            self.backspace()
            return False
        elif var == 260: # kursor w lewo
            self.cursor_left()
            return False
        elif var == 261: # kursor w prawo
            self.cursor_right()
            return False
        elif var == 262: # home
            self.cursor_home()
            return False
        elif var == 360:
            self.cursor_end()
            return False
        elif var == 274:
            self._running = False
            self.text = None
            return False
        elif var > 250 or var < 0:
            return False
            #raise RuntimeError( var )

        if self._only_digits and not var in [ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57 ]:
            return False

        #Tutaj dojdzie, jeśli nie było żadnej innej akcji
        if self._cursor >= self.text_length():
            self.text += chr( var )
        else:
            listtext = list( self.text )
            listtext[ self._cursor ] = chr( var )
            self.text = ''.join( listtext )
        self.cursor_right()
        return True

    def clear(self):
        self._win.clear()
        self._win.refresh()

class ROText(object):
    def __init__(self, y, x, text, title = None, refresh = True, size = None ):
        self._x = x
        self._y = y
        self._title = title
        self.text = text
        if size:
            self._const_size = True
            self._size = size
        else:
            self._size = { 'height' : 3, 'width' : self.text_length() + 2, }
            self._const_size = False
        if refresh:
            self.refresh()

    def refresh(self, bold = True):
        if not self._const_size:
            width = self.text_length() + 2
        else:
            width = self._size['width']

        if bold:
            gflags = curses.A_BOLD
        else:
            gflags = 0

        self._win = curses.newwin( self._size['height'], width, self._y, self._x)
        self._win.nodelay(True)
        self._win.border()
        swidth = self._win.getmaxyx()[1] - 2 #Nie wiem czemu musi być tak 2, ale bez tego nie działa
        if self._title:
            center = ( swidth/2 ) - ( len(self._title)/2 ) + 1
            self._win.addstr( 0, center, self._title.encode( 'utf-8' ), gflags )
        self._win.refresh()
        self._win2 = curses.newpad( self._size['height'] -2, swidth + 1)

        loop = -1
        for line in self.text.encode( 'UTF-8' ).split('\n'):
            try:
                loop += 1
                self._win2.addstr( loop, 0, line[:swidth], gflags )
            except curses.error, er:
                raise RuntimeError( line, loop )

        self._win2.refresh( 0, 0, self._y+1, self._x+1,  self._y+2, self._x+swidth)

    def get_size(self):
        return self._size

    def set_cords(self, x = None, y = None):
        if x != None:
            self._x = x
        if y != None:
            self._y = y

    def clear(self):
        self._win.clear()
        self._win.refresh()

    def run(self):
        self._win.nodelay(False)
        self._win.getch()

    def text_length(self):
        max_length = 0
        for line in self.text.split('\n'):
            if len( line ) > max_length:
                max_length = len( line )
        return max_length
