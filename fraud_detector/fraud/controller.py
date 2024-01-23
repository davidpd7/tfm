import functools

from PyQt6.QtWidgets import  QTableWidgetItem
import pandas as pd

class Controller:

    def __init__(self, view, model):

        self.__view = view
        self.__model = model
        self.buttons = self.__view.get_buttons()
        self.bar_buttons = self.__view.get_bar_buttons()
        self.bar_connetions()

    def bar_connetions(self):
        self.bar_buttons["expmenu"].triggered.connect(self.__model.export_template)
        self.filename = self.bar_buttons["impmenu"].triggered.connect(self.__model.browse_template)
    
    def buttons_connections(self):
        pass    
    