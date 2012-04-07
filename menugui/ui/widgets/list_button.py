# -*- encoding: utf-8 -*-
from menugui.ui.widgets.button import Button
from menugui.ui.list import List
from menugui.elements import ListElement

class ListButton(Button):
    def __init__(self, parent, pos_y, pos_x, label, width, elements_function):
        super(ListButton, self).__init__(parent, pos_y, pos_x, '', width, fun = self.list_function_generator)
        self._elements_function = elements_function
        self.data = None
        self._label = label
    
    def list_function_generator(self, menu):
        glist = List(self._label, self._parent, indexing=False, with_exit=False)
        for key, label in self._elements_function():
            glist.add_option(ListElement(label, key))
        glist.set_element(self.data)
        glist.run()
        self.data = glist.element._data
        return self.data

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if value == None:
            self.set_label(u'(wybierz')
        else:
            for key, label in self._elements_function():
                if key == value:
                    self.set_label(label)
                    break
        self._data = value
