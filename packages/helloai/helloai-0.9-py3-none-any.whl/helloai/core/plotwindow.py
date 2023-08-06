import builtins
import os
if os.name != 'posix':
    from pynput import keyboard

import matplotlib.pyplot as plt
import numpy as np
from helloai import *

__all__ = ['PlotWindow']

class PlotWindow:
    def __init__(self):
        self.__name = 'no-name'
        self.__plt = plt
        # self.__plt.plot([1, 2, 3, 4])
        self.__plt.ylabel('some numbers')
        self.__plt.ion()
        _ = self.__plt.connect('button_press_event', self.__on_mouse)
        _ = self.__plt.connect('key_press_event', self.__on_key)
        _ = self.__plt.connect('close_event', self.__on_close)
        self.__plt.show()
        
    def __del__(self):
        self.__plt.close()

    def __on_mouse(self, event):
        # print('[plot] you pressed', event.button, event.xdata, event.ydata)
        if builtins.mouse_event:
            builtins.mouse_event(self.__name, 21, event.xdata, event.ydata, None, None)
            
    def __on_key(self, event):
        print('[plot] you pressed', event.key, event.xdata, event.ydata)
        key = event.key
        if key == 'escape':
            key = 'esc'
        elif key == 'q' or key == 'Q':
            self.__close_input()

        if hasattr(builtins, 'key_pressed') and builtins.key_pressed:
            builtins.key_pressed(key)

    def __on_close(self, event):
        # self.__close_input()
        pass

    def __close_input(self):
        if os.name != 'posix':
            controler = keyboard.Controller()
            controler.press(keyboard.Key.enter) 
            controler.release(keyboard.Key.enter)

    def show(self):
        self.__plt.draw()
        self.__plt.pause(0.001)
        
    def ylabel(self, label):
        self.__plt.ylabel(label)
        
    def xlabel(self, label):
        self.__plt.xlabel(label)

    def update(self):
        self.__plt.draw()
        self.__plt.pause(0.001)

    def close(self):
        self.__plt.close()
    
    def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
        self.__plt.plot(*args, scalex=scalex, scaley=scaley, data=data, **kwargs)
        self.update()

    def easy_plot(self):
        pass


# wind = PlotWindow()

# x = np.arange(-50, 51)
# for pow in range(1,5):   # plot x^1, x^2, ..., x^4
#     y = [Xi**pow for Xi in x]
#     wind.plot(x, y)
#     delay(1000)
#     # input("Press [enter] to continue.")

# wait_key(0)
# wind.close()
