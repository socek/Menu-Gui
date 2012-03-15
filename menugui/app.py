# -*- encoding: utf-8 -*-
import curses
import locale
from menugui import colors
from menugui.log import LOGGER
from menugui.string import String

class Title(object):
    def __init__(self, stdscr, title):
        maxy, maxx = stdscr.getmaxyx()
        self._win = curses.newwin(1, maxx, 0, 0)
        maxx = self._win.getmaxyx()[1] -2
        self._text = String(title)        
        
        data = self._text.center(maxx)
        self._win.addstr(data, colors.COLORS['main title'])
        self._win.refresh()

    def close(self):
        self._win.clear()

class AppClass(object):

    def __init__(self, title):
        self._stdscr = None
        self._title = None
        self._title_text = title

    def _init(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._stdscr.keypad(1)
        curses.curs_set(0)
        
        colors.init()

        self._title = Title(self._stdscr, self._title_text)

    def run(self, log_path, fun):
        locale.setlocale(locale.LC_ALL,"")
        LOGGER.start(log_path)
        try:
            self._init()
            fun()
        finally:
            LOGGER("Program ended")
            curses.endwin()
            LOGGER.stop()
