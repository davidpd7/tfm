import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow,QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction

from fraud.config import cfg_item

class View(QMainWindow):
     
    def __init__(self):

        super().__init__()
        
        self.setWindowIcon(QIcon(os.path.join(*cfg_item("app","icon_path"))))
        self.setWindowTitle(cfg_item("app","title"))
        self.setFixedSize(*cfg_item("app", "geometry"))
        self.__central_widget = QWidget(self)
        self.__main_layout = QGridLayout(self.__central_widget)
        self.setCentralWidget(self.__central_widget)
        self.__render()

    def __render(self):
   
            self.__add_menubar()
            self.__add_buttons()

    def __add_menubar(self):

        menubar = self.menuBar()
        filemenu = menubar.addMenu(cfg_item("view", "menu_bar", "file_menu", "name"))
        infomenu = menubar.addMenu(cfg_item("view", "menu_bar", "info_menu", "name"))

        impmenu = QAction(cfg_item("view", "menu_bar", "file_menu", "option1"), self)
        expmenu = QAction(cfg_item("view", "menu_bar", "file_menu", "option2"), self)
        imptest = QAction(cfg_item("view", "menu_bar", "file_menu", "option3"), self)
        insmenu = QAction(cfg_item("view", "menu_bar", "info_menu", "option1"), self)
        vermenu = QAction(cfg_item("view", "menu_bar", "info_menu", "option2"), self)

        filemenu.addAction(impmenu)
        filemenu.addAction(expmenu)
        filemenu.addAction(imptest)
        infomenu.addAction(insmenu)
        infomenu.addAction(vermenu)

        self.action_instances = {
            "impmenu": impmenu,
            "expmenu": expmenu,
            "imptest" : imptest,
            "insmenu": insmenu,
            "vermenu": vermenu
        }


    def __set_buttons(self, description):
        
        button = QPushButton(description, parent = self.__central_widget,)
        button_size = QSize(*cfg_item("view", "button_size"))
        style = self.__css_style(cfg_item("view","button_style"))
        button.setFixedSize(button_size)
        button.setStyleSheet(style)
        return button

    def __add_buttons(self):
        self.button_instances = {}
        button_names = cfg_item("view", "push_buttons")

        for name in button_names:
            pos = cfg_item("view", "push_buttons", name, "pos")
            description = cfg_item("view", "push_buttons", name, "name")
            button = self.__set_buttons(description)
            self.__main_layout.addWidget(button, *pos)
            self.button_instances[name] = button
    

    def __css_style(self, styles_data):
        css_style = ""
        for key, value in styles_data.items():
            css_style += f"{key}: {value}; "
        return css_style

    def get_buttons(self):
        return self.button_instances
    
    def get_bar_buttons(self):
        return self.action_instances
        
    
    




    


        



        
    




    

        
    


        
