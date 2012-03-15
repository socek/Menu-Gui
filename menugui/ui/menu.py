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
    _line_template_indexing = u"%%%dd. %%s"
    _line_template = u"%s"
    def __init__(self, title, parent = None, pos_x = None, pos_y = None, width = None, height = None, indexing=True, with_exit=True):
        super(Menu, self).__init__(title=title, parent=parent, pos_x=pos_x, pos_y=pos_y, width=width, height=height)
        self._indexing = indexing
        self._with_exit = with_exit
        self._menu_list = []
        self.rewind()
    
    def _get_line_template(self):
        if self._indexing:
            number_of_elements = len(self.elements)
            return self._line_template_indexing %(len(str(number_of_elements)))
        else:
            return self._line_template

    @property
    def elements(self):
        if self._with_exit:
            return self._menu_list + [MenuObject(u'Exit', self.force_close)]
        else:
            return self._menu_list

    def add_option(self, option):
        option._set_menu(self)
        self._menu_list.append(option)
        
    def _generate_data(self):
        lines = [] + self._data
        width = self.width
        template = self._get_line_template()
        
        first_element = self._actual_first_element
        last_element = self._actual_first_element + self.height - 2 
        elements = self.elements[first_element:last_element]
        loop = first_element - 1
        for element in elements:
            loop += 1
            if self._indexing:
                data = template % (loop+1, element.name)
            else:
                data = (element.name.center(self.width-2))
            
            if loop == self._actual_element_number:
                line = (String(data).full(width-2), element.flags('active'))
            else:
                line = (String(data).full(width-2), element.flags('normal'))
                
            lines.append(line)
        return lines
    
    @property
    def height(self):
        if self._height == None:
            return len(self._data) + len(self.elements)+2
        else:
            return self._height
    
    @property
    def width(self):
        elements_width = len(self._title)
        for line in self._data:
            line = String(line[0])
            elements_width = (elements_width >= len(line) ) and elements_width or len(line)
            
        loop = -1
        template = self._get_line_template()
        for element in self.elements:
            loop += 1
            if self._indexing:
                data = template % (loop+1, element.name)
            else:
                data = template % (element.name)
            elements_width = (elements_width >= len(data) ) and elements_width or len(data)
        return elements_width + 2
    
    def go_begin(self):
        self._actual_element_number = 0
        self._actual_first_element = 0
        self.refresh()
    
    def go_end(self):
        self._actual_element_number = len(self.elements) - 1
        self._actual_first_element = len(self.elements) - self.height + 2 + len(self._data)
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
            self._actual_first_element = len(self.elements) - self.height + 2 + len(self._data)
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
        self.set_active(False)
        self.refresh()
        element = self.element
        element.run()
        self.set_active(True)
        self.refresh()
    
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
        
    def rewind(self):
        self._actual_element_number = 0
        self._actual_first_element = 0
        self._running = True

class List(Menu):
    def __init__(self, *args, **kwargs):
        self._selected_element = None
        super(List, self).__init__(*args, **kwargs)
    
    def get_actual_element(self):
        return self._selected_element

    def run_element(self):
        self._selected_element = self.element._fun
        self.force_close()
    
    def force_close(self, menu = None):
        self._running = False
        self._selected_element = None
