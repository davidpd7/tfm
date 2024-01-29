import os
import re
import joblib

from PyQt6.QtWidgets import QFileDialog
import pandas as pd
from sklearn.metrics import confusion_matrix

from fraud.config import cfg_item

class Model:

    def __init__(self):

        self.__mandatory_columns = cfg_item("template", "columns","mandatory")
        self.__non_mandatory_columns = cfg_item("template", "columns","non_mandatory") 
        self.__running = False
        self.__opt_meandiff = joblib.load(os.path.join(*cfg_item("app","packages", "binning_meandiff")))
        self.__opt_amt = joblib.load(os.path.join(*cfg_item("app","packages","binning_amt")))
        self.__opt_tslt = joblib.load(os.path.join(*cfg_item("app","packages","binning_tslt")))
        self.__preprocessor = joblib.load(os.path.join(*cfg_item("app","packages","preprocessor")))
        self.__lg_model = joblib.load(os.path.join(*cfg_item("app","packages","model_path")))
        self.__mandatory_indicator = cfg_item("app", "mandatory_indicator")
        self.__transaction_column = cfg_item("template","columns", "datetime", "transaction")
        self.__date_of_birth_column = cfg_item("template","columns", "datetime", "date_of_birth")
        self.__amount_column = cfg_item("transformed_data","columns","binned", "amount")
        self.__transaction_age = cfg_item("transformed_data","columns","datetime", "transaction_age")
        self.__transaction_amount_diff = cfg_item("transformed_data","columns","transformations", "transaction_amount_diff")
        self.__time_since_last_transaction = cfg_item("transformed_data","columns","datetime", "time_since_last_transaction")
  
    def __columns_check(self, data):
        if any(data.columns.str.contains(re.escape(self.__mandatory_indicator))):
            data.columns = data.columns.str.replace(self.__mandatory_indicator, "")
        print(data.columns)
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
            data = self.__data_transformation(data)
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

    def __data_transformation(self, data):
                
        transaction_hour = cfg_item("transformed_data","columns","datetime", "transaction_hour")
        transaction_day = cfg_item("transformed_data","columns","datetime", "transaction_day")
        number_days_year = cfg_item("transformed_data","columns","datetime", "number_days_year")
        unix_time = cfg_item("transformed_data","columns","datetime", "unix_time")
        mean_transaction_amount =  cfg_item("transformed_data","columns","transformations", "mean_transaction_amount")
        self.__transaction_amount_diff = cfg_item("transformed_data","columns","transformations", "transaction_amount_diff")
        cc_num =  cfg_item("transformed_data","columns","transformations", "credit_card_number")

        try:
            data[mean_transaction_amount] = data.groupby(cc_num)[self.__amount_column].transform("mean")
            data[self.__transaction_amount_diff] = data[self.__amount_column] - data[mean_transaction_amount]
            data[self.__time_since_last_transaction] = data.groupby("cc_num")[unix_time].diff().fillna(0)
            data[transaction_hour] =  data[self.__transaction_column].dt.hour
            data[transaction_day] = data[self.__transaction_column].dt.dayofweek
            data[self.__transaction_age] = (data[self.__transaction_column] - data[self.__date_of_birth_column]).dt.days // number_days_year
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def __optimal_binning(self, data):

        amount_binned = cfg_item("transformed_data","columns","binned", "amount_binned")
        transaction_amount_diff_binned = cfg_item("transformed_data","columns","binned", "transaction_amount_diff")
        time_since_last_transaction_binned = cfg_item("transformed_data","columns","binned", "time_since_last_transaction")
  
        metric = "bins"
        try:
            data[amount_binned] = self.__opt_amt.transform(data[self.__amount_column], metric=metric)
            data[time_since_last_transaction_binned] = self.__opt_tslt.transform(data[self.__time_since_last_transaction], metric=metric)
            data[transaction_amount_diff_binned] = self.__opt_meandiff.transform(data[self.__transaction_amount_diff], metric=metric)
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
            print(f"Error 3: {e}")
            return None

    def predictor(self):

        self.__data_processed = self.get_data_processed()
        if self.__data_processed is None:
            return None
        self.__predictions = self.__lg_model.predict(self.__data_processed)
        print(self.__predictions)
        return self.__predictions

    def __model_metrics(self):
        pass

    def browse_test(self):
        self.__filetest, _ = QFileDialog.getOpenFileName(None, "Open File")
        self.__test_predictions()

    def __test_predictions(self):
        test = pd.read_csv(self.__filetest, index_col=0)['is_fraud']
        print(confusion_matrix(y_true=test,y_pred=self.__predictions, normalize ='true'))
        
    
