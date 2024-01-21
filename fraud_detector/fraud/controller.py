import functools

from PyQt6.QtWidgets import  QTableWidgetItem

class Controller:

    def __init__(self, view, model):

        self.__view = view
        self.__model = model
        
    