# -*- encoding: utf-8 -*-
import curses

_COLORS = {
    'normal' : (curses.COLOR_WHITE, curses.COLOR_BLACK),
    'highlited' : (curses.COLOR_WHITE, curses.COLOR_CYAN),
    'main title': (curses.COLOR_BLUE, curses.COLOR_WHITE),
}

COLORS = {}

def init(init_colors=None):
    if init_colors == None:
        init_colors = _COLORS
    curses.start_color()
    loop = 0
    for key, element in init_colors.items():
        loop += 1
        curses.init_pair(loop, *element)
        COLORS[key] = curses.color_pair(loop)
