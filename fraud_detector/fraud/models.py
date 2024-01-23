import os
import re
from time import sleep

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths
import pandas as pd
import numpy as np
from datetime import datetime

from fraud.config import cfg_item

class Model:

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
        sleep(self.sleep_time)
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
        template.to_csv(cfg_item("template","name"))

    def browse_template(self):
        self.fileName, _ = QFileDialog.getOpenFileNames(None, 'Open File')
        return self.fileName
 