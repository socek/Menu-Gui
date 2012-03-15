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
        loop = -1
        lines = []
        number_of_elements = len(self.elements)
        template = self._line_template %(len(str(number_of_elements)))
        width = self.width
        for element in self.elements:
            loop += 1
            data = template % (loop, element.name)
            
            if loop == self._actual_element_number:
                line = (String(data).full(width-2), element.flags('active'))
            else:
                line = (String(data).full(width-2), element.flags('normal'))
                
            lines.append(line)
        
        return lines
    
    @property
    def height(self):
        return len(self._menu_list)+3
    
    @property
    def width(self):
        elements_width = len(self._title)
        loop = -1
        number_of_elements = len(self._menu_list)
        template = self._line_template %(len(str(number_of_elements)))
        for element in self.elements:
            loop += 1
            data = template % (loop, element.name)
            elements_width = (elements_width >= len(data) ) and elements_width or len(data)
            self._elements_width = elements_width
        return self._elements_width + 2
    #
    #def refresh_width(self):
    #    if self._list:
    #        end = len( self._menu_list )
    #    else:
    #        end = len( self._menu_list ) + 1
    #    max_width = self._width
    #    for loop in range( end ):
    #        if len( self._menu_list ) == loop:
    #            name = 'Exit'
    #        else:
    #            name = self._menu_list[loop].name
    #        name = "%d.%s" % (loop+1, name )
    #        text_width = len( name ) + 2
    #        if text_width > max_width: max_width = text_width
    #    title_width = len( self._title ) + 2
    #    if  title_width > max_width: max_width = title_width
    #    if max_width > self._width:
    #        self._width = max_width
    #        self._win = curses.newwin( self._get_end() , self._width, self._y, self._x )
    #
    #def go_up(self):
    #    if self._list:
    #        end = len( self._menu_list ) - 1
    #    else:
    #        end = len( self._menu_list )
    #    self._number -= 1
    #    if self._number < 0:
    #        self._number = end
    #    self.refresh()
    #
    #def go_down(self):
    #    if self._list:
    #        end = len( self._menu_list ) - 1
    #    else:
    #        end = len( self._menu_list )
    #    self._number += 1
    #    if self._number > end:
    #        self._number = 0
    #    self.refresh()
    #
    #def run_item(self):
    #    if self._number == len(self._menu_list):
    #        self._running = False
    #    else:
    #        item = self._menu_list[ self._number ]
    #        self.refresh(False)
    #        item.run()
    #
    #def refresh(self, bold = True):
    #    self._win.erase()
    #    self.refresh_width()
    #    self._win.border()
    #
    #    main_width = self._win.getmaxyx()[1] - 2 #Usuwanie linijek po bokach
    #
    #    if bold:
    #        gflags = curses.A_BOLD
    #    else:
    #        gflags = 0
    #
    #    if self._title != None:
    #        if type( self._title ) == unicode:
    #            title = self._title.encode( 'utf-8')
    #        else:
    #            title = self._title
    #        center = ( main_width/2 ) - ( len(title)/2 ) + 1
    #        self._win.addstr( 0, center, title, gflags )
    #
    #    if self._list:
    #        end = len( self._menu_list )
    #    else:
    #        end = len( self._menu_list ) + 1
    #
    #    for loop in range( end ):
    #        if self._number == loop:
    #            color = 2
    #        else:
    #            color = 1
    #
    #
    #        if len( self._menu_list ) == loop:
    #            name = 'Exit'
    #        else:
    #            name = self._menu_list[loop].name
    #
    #        if self._center:
    #            #usuwanie numerku i kropki szerokosci, aby numerki byly zawsze z lewej
    #            width = main_width - len( "%d." % (loop+1) )
    #            name = name.center( width )
    #        if type( name ) == unicode:
    #            name = name.encode( 'utf-8')
    #        name = "%d.%s" % (loop+1, name )
    #
    #        flags = curses.color_pair(color) | gflags
    #
    #        self._win.addstr( loop+1, 1, name, flags )
    #
    #    self._win.refresh()
    #
    
    def go_begin(self):
        self._actual_element_number = 0
        self.refresh()
    
    def go_end(self):
        self._actual_element_number = len( self.elements ) - 1
        self.refresh()
    
    def go_up(self):
        end = len( self.elements ) - 1
        self._actual_element_number -= 1
        if self._actual_element_number < 0:
            self._actual_element_number = end
        self.refresh()
    
    def go_down(self):
        end = len( self.elements ) - 1
        self._actual_element_number += 1
        if self._actual_element_number > end:
            self._actual_element_number = 0
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
            
        self.close()
    
    def force_close(self, menu = None):
        self._running = False
        
    def run_element(self):
        element = self.element
        element.run()
        
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
        self._running = True
