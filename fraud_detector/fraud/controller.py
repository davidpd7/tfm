import functools

from PyQt6.QtWidgets import  QTableWidgetItem
import pandas as pd

class Controller:

    def __init__(self, view, model):

        self.__view = view
        self.__model = model
        self.__buttons = self.__view.get_buttons()
        self.__bar_buttons = self.__view.get_bar_buttons()
        self.bar_connetions()
        self.buttons_connections()

    def bar_connetions(self):
        self.__bar_buttons["expmenu"].triggered.connect(self.__model.export_template)
        self.__bar_buttons["impmenu"].triggered.connect(self.__model.browse_template)
        self.__bar_buttons["imptest"].triggered.connect(self.__model.browse_test)
    
    def buttons_connections(self):
        self.__buttons['push_buttons1'].clicked.connect(self.__model.predictor)
        self.__buttons['push_buttons2'].clicked.connect(self.__model.get_data_processed)
    