import os
import re
from PyQt6.QtWidgets import QFileDialog
import pandas as pd
import numpy as np
import joblib

from fraud.config import cfg_item

class Model:

    def __init__(self):

        self.__mandatory_columns = cfg_item("template", "columns","mandatory_columns")
        self.__non_mandatory_columns = cfg_item("template", "columns","non_mandatory_columns") 
        self.__running = False
        self.__opt_age = joblib.load(os.path.join(*cfg_item("app","packages", "binning_age")))
        self.__opt_amt = joblib.load(os.path.join(*cfg_item("app","packages","binning_amt")))
        self.__preprocessor = joblib.load(os.path.join(*cfg_item("app","packages","preprocesor")))
        self.__lg_model = joblib.load(os.path.join(*cfg_item("app","packages","model_path")))
        self.__mandatory_indicator = cfg_item("app", "mandatory_indicator")
  
    def __columns_check(self, data):
        if any(data.columns.str.contains(re.escape(self.__mandatory_indicator))):
            data.columns = data.columns.str.replace(re.escape(self.__mandatory_indicator), "")
        return True
       
    def export_template(self):
        mandatory_columns = [i + self.__mandatory_indicator for i in self.__mandatory_columns]
        template = pd.DataFrame(columns = mandatory_columns + self.__non_mandatory_columns)
        return template.to_csv(cfg_item("template","name"))

    def browse_template(self):

        self.__running = True
        self.__fileName, _ = QFileDialog.getOpenFileName(None, "Open File")

    def __get_data(self):

        if self.__running:
            data = pd.read_csv(self.__fileName, index_col=0)
            if self.__columns_check(data):
                if not data.empty:
                    return data
        else:
            return None

    def get_data_processed(self):
        data = self.__get_data()
        if data is None:
            return data
        if self.__datetime_check(data):
            data = self.__time_variables(data)
            data = self.__optimal_binning(data)

            self.__data_processed = self.__pipeline(data)
            return self.__data_processed
    
    def __datetime_check(self,data):
        date_time_columns = cfg_item("template", "columns","datetime_columns")
        try:
            for column in date_time_columns:
                data =  pd.to_datetime(data[column])
            return True
        except:
           print("Hello")

    def __time_variables(self, data):
        
        datetime_column = "trans_date_trans_time"
        date_of_birth_column = "dob"
        transaction_hour_column = "trasaction_hour"
        transaction_day_column ="trasaction_day"
        transaction_age = "age"
        number_days_year = 365

        try:
            data[transaction_hour_column] =  data[datetime_column].dt.hour
            data[transaction_day_column] = data[datetime_column].dt.dayofweek
            data[transaction_age] = (data[datetime_column] - data[date_of_birth_column]).dt.days // number_days_year
            return data
        except:
            print("Error 1")
        
    
    def __optimal_binning(self, data):

        try:
            data["amt_binned"] = self.__opt_amt.transform(data["amt"], metric="bins")
            data["age_binned"] = self.__opt_age.transform(data["age"], metric="bins")
            return data
        except:
            print("Error 2")
    
    def __pipeline (self, data):

        try:
            numerical_cols = cfg_item("transformed_data","columns", "numerical_cols")
            categorical_cols = cfg_item("transformed_data","columns", "categorical_cols")
            data_processed =  self.__preprocessor.transform(data[numerical_cols + categorical_cols])
            return data_processed
        except:
            print("Error 3")

    def predictor(self):

        self.__data_processed = self.get_data_processed()
        if self.__data_processed is None:
            return None
        predictions = self.__lg_model.predict(self.__data_processed)
        print(predictions)
        return predictions

    def __model_metrics(self):
        pass