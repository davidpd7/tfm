import joblib
import os
from importlib import resources

from fraud.assets.config.config import cfg_item

class Packages():

    __root_dir = "packages"

    def __init__(self):
        
        self.__load_packages()
        
    def __load_packages(self):
            
            for package_type in ["models", "transformers"]:
                for package_name, package_info in cfg_item(Packages.__root_dir, package_type).items():
                    package_path = package_info["path"]
                    with resources.path(package_path[0], package_path[1]) as package_file:
                        setattr(self, package_name, joblib.load(package_file))
            

    def get_opt_meandiff(self):
 
        return self.binning_meandiff

    def get_opt_amt(self):

        return self.binning_amt

    def get_opt_tslt(self):

        return self.binning_tslt

    def get_preprocessor(self):

        return self.preprocessor

    def get_model_1(self):

        return self.model_1

    def get_model_2(self):

        return self.model_2

    def get_model_3(self):

        return self.model_3