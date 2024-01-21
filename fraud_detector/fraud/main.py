import os
import time

from fraud.config import cfg_item

from PyQt6.QtWidgets import QFileDialog

import pandas as pd

class App():
    
    def __init__(self):

        self.initial_text = cfg_item("app", "initial_text")
        self.sleep_time = 1
        self.selection_text = cfg_item("app", "selection_text")
        self.error_text = cfg_item("app", "error_text")
        self.browse_text = cfg_item("app", "browse_text")
        self.template_columns = [cfg_item("template", "columns")]
        self.ready_text = cfg_item("template", "ready_text")
        
    def welcome(self):
        print(self.initial_text)
        time.sleep(self.sleep_time)
        self.run()

    def run(self):
        
        print(self.selection_text)
        answer = str.lower(input())
        if answer == "y":
            self.export_template()
        elif answer == "n":
            print(self.browse_text)
            self.run()
        elif answer == "s":
            pass
        else:
            print(self.error_text)
            self.run()


    def get_data(self):
        pass

    def stop(self):
        pass

    def export_template(self):
        
        template = pd.DataFrame(columns = self.template_columns)
        template.to_csv("template_fraud.csv")
        print(self.ready_text)
        self.browse_template()


    def browse_template(self):

        answer = str.lower(input())
        if answer == "r":
           self.fileName, _ = QFileDialog.getOpenFileNames(None, 'Open File')
           print(self.fileName)
        if answer == "s":
            self.stop()
        else:
            print(cfg_item("app", "error_text"))
            self.browse_template()
    