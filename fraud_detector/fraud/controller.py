import functools

from PyQt6.QtWidgets import  QTableWidgetItem, QMessageBox
import numpy as np

from fraud.config import cfg_item
class Controller:

    def __init__(self, view, model):

        self.__view = view
        self.__model = model
        self.__buttons = self.__view.get_buttons()
        self.__bar_buttons = self.__view.get_bar_buttons()
        self.__combo_box = self.__view.get_combo_box()
        self.__bar_connetions()
        self.__buttons_connections()

    def __bar_connetions(self):
        self.__bar_buttons["expmenu"].triggered.connect(self.__model.export_template)
        self.__bar_buttons["impmenu"].triggered.connect(self.__model.browse_template)
        self.__bar_buttons["imptest"].triggered.connect(self.__model.browse_test)
        self.__bar_buttons["exppred"].triggered.connect(self.__model.export_predictions)
  
    def __buttons_connections(self):
        self.__buttons["push_buttons1"].clicked.connect(self.__on_button1_clicked)
        self.__buttons["push_buttons2"].clicked.connect(self.__on_button2_clicked)
        self.__buttons["push_buttons3"].clicked.connect(self.__on_button3_clicked)

    def __on_button1_clicked(self):
        result_correct_transactions = "Number non-fraudulent Transaction:"
        result_fraudulent_transaction = "Number Fraudulent Transaction:"
        current_text = self.__combo_box.currentText()
        for model in cfg_item("app","packages","models"):
            if current_text == cfg_item("app","packages","models", model, "name"):
                model =  cfg_item("app","packages","models","model_1","code")
        result = self.__model.predictor(model)
        if result is not None:   
            counts = np.bincount(result, minlength=2)
            result = f"{result_correct_transactions} {counts[0]}\n{result_fraudulent_transaction} {counts[1]}"
            self.__view.display_message(result, "push_buttons1")

    def __on_button2_clicked(self):
        try:
            self.__model.get_data_processed()
        except:
            None    

    def __on_button3_clicked(self):
        try:
            result = self.format_confusion_matrix(self.__model.compare_results())
            self.__view.display_message(result, "push_buttons3")
        except:
            None
    
    def format_confusion_matrix(self, matrix):
        descriptions = [
            "True Negative (TN): Correctly predicted non-fraudulent transactions",
            "False Positive (FP): Incorrectly predicted fraudulent transactions",
            "False Negative (FN): Incorrectly predicted non-fraudulent transactions",
            "True Positive (TP): Correctly predicted fraudulent transactions"
        ]

        result_str = ""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                percentage = matrix[i, j] * 100
                result_str += f"{descriptions[i * len(matrix) + j]}: {percentage:.2f}%\n"

        return result_str
    

        
    

    