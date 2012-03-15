# -*- encoding: utf-8 -*-
from time import sleep
import curses
from menugui.ui.window import Window
from menugui.string import forceUnicode, String
from menugui.colors import COLORS

class MenuObject(object):
    color = {
        'normal' : 'normal',
        'active' : 'highlited',
    }
    def __init__(self, name, fun):
        self._name = forceUnicode(name)
        self._fun = fun
        self._menu = None

    def _set_menu(self, menu):
        self._menu = menu

    @property
    def name(self):
        return self._name

    def run(self):
        if self._fun == None:
            pass
        else:
            self._fun(self._menu)
    
    def flags(self, state):
        name = self.color[state]
        return COLORS[name]
    
class Menu(Window):
    _line_template = u"%%%dd. %%s" 
    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self._menu_list = []
        self._elements_width = 0
        self.rewind()

    #def move(self, y, x ):
    #    self._win.mvwin( y, x )
    #    self.refresh()
    #
    #def _get_end(self):
    #    if self._list:
    #        return len( self._menu_list ) + 2
    #    else:
    #        return len( self._menu_list ) + 3
    
    @property
    def elements(self):
        return self._menu_list + [MenuObject(u'Exit', self.force_close)]

    def add_option(self, option):
        option._set_menu(self)
        self._menu_list.append(option)
        
    def _generate_data(self):
        lines = []
        number_of_elements = len(self.elements)
        template = self._line_template %(len(str(number_of_elements)))
        width = self.width
        
        first_element = self._actual_first_element
        last_element = self._actual_first_element + self.height - 2 
        elements = self.elements[first_element:last_element]
        loop = first_element - 1
        for element in elements:
            loop += 1
            data = template % (loop+1, element.name)
            
            if loop == self._actual_element_number:
                line = (String(data).full(width-2), element.flags('active'))
            else:
                line = (String(data).full(width-2), element.flags('normal'))
                
            lines.append(line)
        return lines
    
    @property
    def height(self):
        if self._height == None:
            return len(self._menu_list)+3
        else:
            return self._height
    
    @property
    def width(self):
        elements_width = len(self._title)
        loop = -1
        number_of_elements = len(self._menu_list)
        template = self._line_template %(len(str(number_of_elements)))
        for element in self.elements:
            loop += 1
            data = template % (loop+1, element.name)
            elements_width = (elements_width >= len(data) ) and elements_width or len(data)
            self._elements_width = elements_width
        return self._elements_width + 2
    
    def go_begin(self):
        self._actual_element_number = 0
        self._actual_first_element = 0
        self.refresh()
    
    def go_end(self):
        self._actual_element_number = len(self.elements) - 1
        self._actual_first_element = len(self.elements) - self.height + 2
        self.refresh()
    
    def go_up(self):
        end = len( self.elements ) - 1
        self._actual_element_number -= 1
        if self._actual_element_number < 0:
            self.go_end()
        
        if self._actual_element_number < self._actual_first_element:
            self._actual_first_element = self._actual_element_number
        
        self.refresh()
    
    def go_down(self):
        end = len( self.elements ) - 1
        self._actual_element_number += 1
        if self._actual_element_number > end:
            self.go_begin()
        
        if self._actual_element_number - self._actual_first_element >= (self.height-2):
            self._actual_first_element += 1
        
        self.refresh()
    
    def go_page_down(self):
        self._actual_first_element += self.height - 2
        if len(self.elements) - self._actual_first_element < self.height - 2:
            self._actual_first_element = len(self.elements) - self.height + 2
        self._actual_element_number = self._actual_first_element
        self.refresh()
    
    def go_page_up(self):
        self._actual_first_element -= self.height - 2
        if self._actual_first_element < 0:
            self._actual_first_element = 0
        self._actual_element_number = self._actual_first_element
        self.refresh()
    
    @property
    def element(self):
        return self.elements[self._actual_element_number]
    
    def run(self):
        self._running = True
        self.set_active(True)
        self.refresh()
        while self._running:
            # 259 - up
            # 258 - down
            # 262 - Home
            # 360 - End
            # 10 - enter
            self._c_window.keypad(1)
            self._char = self._c_window.getch()
            if self._char == curses.KEY_DOWN:       self.go_down()
            elif self._char == curses.KEY_UP:       self.go_up()
            elif self._char == 10:                  self.run_element()
            elif self._char == curses.KEY_HOME:     self.go_begin()
            elif self._char == curses.KEY_END:      self.go_end()
            elif self._char == curses.KEY_NPAGE:    self.go_page_down()
            elif self._char == curses.KEY_PPAGE:    self.go_page_up()
            
        self.close()
    
    def force_close(self, menu = None):
        self._running = False
        
    def run_element(self):
        element = self.element
        element.run()
    
    def refresh(self):
        super(Menu, self).refresh(False)
        
        pos_y = self.height - 2
        pos_x = 0
        flags = 0
        if self._actual_first_element + self.height - 2 < len(self.elements):
            char = curses.ACS_DARROW
        else:
            char = curses.ACS_VLINE
        self._c_window.addch(pos_y, pos_x, char, flags)
        
        if self.height <= 3:
            pos_x = self.width - 1
        pos_y = 1
        if self._actual_first_element != 0:
            char = curses.ACS_UARROW
        else:
            char = curses.ACS_VLINE
        self._c_window.addch(pos_y, pos_x, char, flags)
        self._c_window.refresh()
        
    #def run(self):
    #    if self._list == False:
    #        self._number = 0
    #    ret = None
    #    self._running = True
    #    self.refresh()
    #    while self._running:
    #        # 259 - up
    #        # 258 - down
    #        # 262 - Home
    #        # 360 - End
    #        # 10 - enter
    #        self._win.keypad(1)
    #        self._char = self._win.getch()
    #        if self._char == 259:
    #            self.go_up()
    #        elif self._char == 258:
    #            self.go_down()
    #        elif self._char == 10:
    #            if self._list:
    #                self._running = False
    #                ret = self._menu_list[ self._number ]._name
    #            else:
    #                self.run_item()
    #        elif self._char == 360:
    #            self._number = len( self._menu_list )
    #            if self._list: self._number -= 1
    #        elif self._char == 262:
    #            self._number = 0
    #        #else:
    #        #    raise RuntimeError( self._char )
    #        self.refresh()
    #        sleep( 0.01)
    #    self.close()
    #    return ret
    #
    #def close(self):
    #    self._win.erase()
    #    self._win.refresh()
    #    if self._menu != None:
    #        self._menu.refresh(False)
    #
    
    def rewind(self):
        self._actual_element_number = 0
        self._actual_first_element = 0
        self._running = True
