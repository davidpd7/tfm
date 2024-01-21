import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow,QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget
from PyQt6.QtCore import QUrl, QSize, Qt
from PyQt6.QtGui import QDesktopServices, QPixmap

from fraud.config import cfg_item


class View(QMainWindow):
     
    def __init__(self):

        super().__init__()
        
        self.setWindowIcon(QIcon(os.path.join(*cfg_item("app","icon_path"))))
        self.setWindowTitle(cfg_item("app","title"))
        
        self.__central_widget = QWidget(self)
        
        self.__main_layout = QGridLayout(self.__central_widget)
        self.setCentralWidget(self.__central_widget)

        self.__add_buttons()
        self.__create_table()


    def __set_buttons(self, description):
        
        button = QPushButton(description, parent = self.__central_widget,)
        icon_size = QSize(*cfg_item("view", "icon_size"))
        button_size = QSize(*cfg_item("view", "button_size"))
        style = self.__css_style(cfg_item('view','button_style'))
        button.setIconSize(icon_size)
        button.setFixedSize(button_size)
        button.setStyleSheet(style)
        return button

    def __add_buttons(self):
        button_names = cfg_item("view","push_buttons")
        for name in button_names:
            pos = cfg_item("view","push_buttons",name, "pos")
            description = cfg_item("view","push_buttons", name, "name")
            button = self.__set_buttons(description)
            self.__main_layout.addWidget(button, *pos)
    
    def __create_table(self):
        self.__tables = {}
        table_name = cfg_item("view", "tables", "name")
        self.__tables[table_name] = QTableWidget()
        self.__main_layout.addWidget(self.__tables[table_name])

    
    def __css_style(self, styles_data):
        css_style = ""
        for key, value in styles_data.items():
            css_style += f"{key}: {value}; "
        return css_style
        
        
    
    




    


        



        
    




    

        
    


        
