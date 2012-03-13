# -*- encoding: utf-8 -*-
import curses
from string import String
import locale
from log import LOGGER

class Title(object):
    def __init__(self, stdscr, title):
        maxy, maxx = stdscr.getmaxyx()
        self._win = curses.newwin(1, maxx, 0, 0)
        maxx = self._win.getmaxyx()[1] -2
        self._text = String(title)        
        
        data = self._text.center(maxx)
        self._win.addstr(data, curses.color_pair(2))
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
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

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
