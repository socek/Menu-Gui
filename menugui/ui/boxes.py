from menugui.ui.window import Window
from menugui.ui.widgets.button import Button

class InfoBox(Window):
    def __init__(self, title, text, *args, **kwargs):
        super(InfoBox, self).__init__(title, *args, **kwargs)
        texts = text.split('\n')
        for text in texts:
            self._data.append((text, 0))
        self._data.append(('', 0))
        
        button_text = u'ok'
        button_width = len(button_text) + 2
        button_margin = (self.width / 2) - (button_width / 2) 
        
        self.button = Button(self, self.height-2, button_margin, button_text, button_width, self.peacful_close)
        self.button.set_active(True)
        self.button.set_highlited(True)
        
        self.run()
    
    def run(self):
        self._running = True
        self.set_active(True)
        
        self.refresh()
        while self._running:
            self.button.processed_character()
        
        self.close()
    
    def peacful_close(self, *args, **kwargs):
        self._running = False

class QuestionBox(Window):
    def __init__(self, title, text, *args, **kwargs):
        super(QuestionBox, self).__init__(title, *args, **kwargs)
        texts = text.split('\n')
        for text in texts:
            self._data.append((text, 0))
        
        button_texts = (u'tak', u'nie')
        text_width = 0
        for text in button_texts:
            if text_width < len(text):
                text_width = len(text)
            self._data.append(('', 0))
        
        button_width = text_width + 2
        button_margin = (self.width / 2) - (button_width / 2)
        
        self._actual_element_number = 1
        
        self._buttons = []
        for button_text in button_texts:
            pos_y = self.height - 1 - ( len(button_texts) - button_texts.index(button_text))
            button = Button(self, pos_y, button_margin, button_text, button_width, self.peacful_close)
            self._buttons.append(button)
        
    def run(self):
        self._running = True
        self.set_active(True)
        
        self.refresh()
        while self._running:
            key = self._active_button.processed_character()
            if key  == None:
                pass
            elif key[0] == 262: # home
                self.go_begin()
            elif key[0] == 360: # end
                self.go_end()
            elif key[0] == 259: # cursor up
                self.go_up()
            elif key[0] == 258: # cursor down
                self.go_down()
            else:
                print key
            self.refresh()
        
        self.close()
        
        if self._actual_element_number == 0:
            return True
        else:
            return False
    
    @property
    def _active_button(self):
        return self._buttons[self._actual_element_number]
    
    def refresh(self, window_refresh=True):
        super(QuestionBox, self).refresh(False)
        
        for button in self._buttons:
            button.set_active(self._active)
            if button == self._active_button:
                button.set_highlited(True)
            else:
                button.set_highlited(False)
            button.refresh()
        
        self._c_window.refresh()
    
    def peacful_close(self, *args, **kwargs):
        self._running = False
    
    def go_begin(self):
        self._actual_element_number = 0
    
    def go_end(self):
        self._actual_element_number = len(self._buttons) - 1
    
    def go_up(self):
        end = len(self._buttons) - 1
        self._actual_element_number -= 1
        if self._actual_element_number < 0:
            self._actual_element_number = 0
    
    def go_down(self):
        end = len(self._buttons) - 1
        self._actual_element_number += 1
        if self._actual_element_number > end:
            self._actual_element_number = end
