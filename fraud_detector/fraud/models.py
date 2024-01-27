import os
import re
import joblib

from PyQt6.QtWidgets import QFileDialog
import pandas as pd

from fraud.config import cfg_item

class Model:

    def __init__(self):

        self.__mandatory_columns = cfg_item("template", "columns","mandatory")
        self.__non_mandatory_columns = cfg_item("template", "columns","non_mandatory") 
        self.__running = False
        self.__opt_age = joblib.load(os.path.join(*cfg_item("app","packages", "binning_age")))
        self.__opt_amt = joblib.load(os.path.join(*cfg_item("app","packages","binning_amt")))
        self.__preprocessor = joblib.load(os.path.join(*cfg_item("app","packages","preprocessor")))
        self.__lg_model = joblib.load(os.path.join(*cfg_item("app","packages","model_path")))
        self.__mandatory_indicator = cfg_item("app", "mandatory_indicator")
        self.__transaction_column = cfg_item("template","columns", "datetime", "transaction")
        self.__date_of_birth_column = cfg_item("template","columns", "datetime", "date_of_birth")
        self.__transaction_age = cfg_item("transformed_data","columns","datetime", "transaction_age")
  
    def __columns_check(self, data):
        if any(data.columns.str.contains(re.escape(self.__mandatory_indicator))):
            data.columns = data.columns.str.replace(self.__mandatory_indicator, "")
        if all(col in data.columns for col in self.__mandatory_columns + self.__non_mandatory_columns):
            return True
        else:
            print("Please import the correct template.")
       
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
        date_time_columns = [self.__transaction_column, self.__date_of_birth_column]
        try:
            for column in date_time_columns:
                data[column] =  pd.to_datetime(data[column])
            return True
        except Exception as e:
            print(f"Error: {e}")
            return None

    def __time_variables(self, data):
                
        transaction_hour = cfg_item("transformed_data","columns","datetime", "transaction_hour")
        transaction_day = cfg_item("transformed_data","columns","datetime", "transaction_day")
        number_days_year = cfg_item("transformed_data","columns","datetime", "number_days_year")
        
        try:
            data[transaction_hour] =  data[self.__transaction_column].dt.hour
            data[transaction_day] = data[self.__transaction_column].dt.dayofweek
            data[self.__transaction_age] = (data[self.__transaction_column] - data[self.__date_of_birth_column]).dt.days // number_days_year
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def __optimal_binning(self, data):

        amount = cfg_item("transformed_data","columns","binned", "amount")
        amount_binned = cfg_item("transformed_data","columns","binned", "amount_binned")
        age_binned = cfg_item("transformed_data","columns","binned", "age_binned")
        metric = "bins"
        try:
            data[amount_binned] = self.__opt_amt.transform(data[amount], metric=metric)
            data[age_binned] = self.__opt_age.transform(data[self.__transaction_age], metric=metric)
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def __pipeline (self, data):

        numerical_cols = cfg_item("transformed_data","columns", "numerical")
        categorical_cols = cfg_item("transformed_data","columns", "categorical")
        try:
            data_processed =  self.__preprocessor.transform(data[numerical_cols + categorical_cols])
            return data_processed
        except Exception as e:
            print(f"Error: {e}")
            return None

    def predictor(self):

        self.__data_processed = self.get_data_processed()
        if self.__data_processed is None:
            return None
        predictions = self.__lg_model.predict(self.__data_processed)
        print(predictions)
        return predictions

    def __model_metrics(self):
        pass
