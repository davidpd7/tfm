import os

from PyQt6.QtWidgets import QFileDialog
import pandas as pd
import numpy as np
import joblib

from fraud.config import cfg_item

class Model:

    def __init__(self):

        self.template_mandatory_columns = cfg_item("template", "columns","mandatory_columns")
        self.template_non_mandatory_columns = cfg_item("template", "columns","non_mandatory_columns") 
        self.__running = False
        self.__run()
    
    def __run(self):
 
        self.__load_packages()

    def export_template(self):

        template = pd.DataFrame(columns = self.template_mandatory_columns + self.template_non_mandatory_columns)
        return template.to_csv(cfg_item("template","name"))

    def browse_template(self):

        self.__running = True
        self.fileName, _ = QFileDialog.getOpenFileName(None, 'Open File')
  
    def __get_data(self):
        if self.__running:
            data = pd.read_csv(self.fileName, index_col=0)
            if any(data.columns.str.contains(r"\(*\)")):
               data.columns = data.columns.str.replace("(*)","")
            return data

    def predictor(self):

        predictions = self.__lg_model.predict(self.__data_processed)
        print(predictions)
        return predictions

    def get_data_processed(self):
        
        self.__data_processed = self.__pipeline()

    def __time_variables(self):

        data = self.__get_data()
        if data.empty:
            assert False
        try:
            data['trasaction_hour'] = pd.to_datetime(data['trans_date_trans_time']).dt.hour
            data['trasaction_day'] = pd.to_datetime(data['trans_date_trans_time']).dt.dayofweek
            data['dob'] = pd.to_datetime(data['dob'])
            data['trans_date_trans_time'] = pd.to_datetime(data['trans_date_trans_time'])
            data['age'] = (data['trans_date_trans_time'] - data['dob']).dt.days // 365
            return data
        except:
            print("Error 1")
    
    def __load_packages(self):

        self.__opt_age = joblib.load(os.path.join(*cfg_item("app","packages", "binning_age")))
        self.__opt_amt = joblib.load(os.path.join(*cfg_item("app","packages","binning_amt")))
        self.__preprocessor = joblib.load(os.path.join(*cfg_item("app","packages","preprocesor")))
        self.__lg_model = joblib.load(os.path.join(*cfg_item("app","packages","model_path")))
    
    def __optimal_binning(self):
        try:
            data = self.__time_variables()
            data['amt_binned'] = self.__opt_amt.transform(data["amt"], metric='bins')
            data['age_binned'] = self.__opt_age.transform(data["age"], metric='bins')
            return data
        except:
            print("Error 2")
    
    def __pipeline (self):
        try:
            numerical_cols = cfg_item("transformed_data","columns", "numerical_cols")
            categorical_cols = cfg_item("transformed_data","columns", "categorical_cols")
            data = self.__optimal_binning()
            data_processed =  self.__preprocessor.transform(data[numerical_cols + categorical_cols])
            return data_processed
        except:
            "Error 3"

    def __model_metrics(self):
        pass