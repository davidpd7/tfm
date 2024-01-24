import os


from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths
import pandas as pd
import numpy as np
import joblib

from fraud.config import cfg_item

class Model:

    def __init__(self):

        self.template_columns_cat = cfg_item("template", "columns","categorical_cols")
        self.template_columns_con = cfg_item("template", "columns","numerical_cols")
        self.ready_text = cfg_item("template", "ready_text")        
        self.__running = False

    def __get_data(self):
        if self.__running is True:
            data = pd.read_csv(self.fileName, index_col=0)
            return data
    
    def export_template(self):
        template = pd.DataFrame(columns = self.template_columns_cat + self.template_columns_con)
        template.to_csv(cfg_item("template","name"))

    def browse_template(self):
        self.__running = True
        self.fileName, _ = QFileDialog.getOpenFileName(None, 'Open File')

    def predictor(self):
        self.lg_model = joblib.load(os.path.join(*cfg_item("app","model_path")))
        print(self.lg_model.predict(self.data_processed))

    def get_data_processed(self):
        
        self.data_processed = self.__pipeline()

    def __time_variables(self):
        data = self.__get_data()
        data['trasaction_hour'] = pd.to_datetime(data['trans_date_trans_time']).dt.hour
        data['trasaction_day'] = pd.to_datetime(data['trans_date_trans_time']).dt.dayofweek
        data['dob'] = pd.to_datetime(data['dob'])
        data['trans_date_trans_time'] = pd.to_datetime(data['trans_date_trans_time'])
        data['age'] = (data['trans_date_trans_time'] - data['dob']).dt.days // 365
        return data
    
    def __optimal_binning(self):

        data = self.__time_variables()
        opt_age = joblib.load(os.path.join(*cfg_item("app","binning_age")))
        opt_amt = joblib.load(os.path.join(*cfg_item("app","binning_amt")))
        data['amt_binned'] = opt_amt.transform(data["amt"], metric='bins')
        data['age_binned'] = opt_age.transform(data["age"], metric='bins')
        return data
    
    def __pipeline (self):

        numerical_cols = ['lat', 'long', 'city_pop', 'unix_time', 'merch_lat', 'merch_long',"trasaction_hour"]
        categorical_cols = ['gender', 'category', 'age_binned', "amt_binned", "trasaction_day"]
        data = self.__optimal_binning()
        preprocessor = joblib.load(os.path.join(*cfg_item("app","preprocesor")))
        data_processed =  preprocessor.transform(data[numerical_cols + categorical_cols])
        
        return data_processed
        
    
