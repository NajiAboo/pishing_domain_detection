import os

from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src import logger
from src.util import read_yaml
from pathlib import Path
import pandas as pd
import collections
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionConfig, data_validation_artifact: DataValidationConfig) -> None:
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.model_schema_info = read_yaml(Path("config/model.yaml"))
        self.schema_columns = self.model_schema_info["columns"]
        
    def __is_train_test_file_exists(self)->bool:
        
        logger.info("Checking if training and test file is available")
        is_train_file_exist = False
        is_test_file_exist = False
        train_file_path = self.data_ingestion_artifact.ingected_train_file_path
        test_file_path = self.data_ingestion_artifact.ingected_test_file_path
        is_train_file_exist = os.path.exists(train_file_path)
        is_test_file_exist = os.path.exists(test_file_path)
        is_available =  is_train_file_exist and is_test_file_exist
        logger.info(f"Is train and test file exists?-> {is_available}")
        
        if not is_available:
            training_file = self.data_ingestion_artifact.ingected_train_file_path
            testing_file = self.data_ingestion_artifact.ingected_test_file_path
            message=f"Training file: {training_file} or Testing file: {testing_file}" \
                "is not present"
            raise Exception(message)
        
        return is_available
    
    def __check_number_of_columns(self, df_input: pd.DataFrame) -> bool:
        
        is_column_match = False
        column_count = len(df_input.columns)
        schema_columns_count = len(self.schema_columns)
        print(f"schema column count {schema_columns_count}")
        
        if column_count == schema_columns_count:
            is_column_match = True
        
        else:
            raise Exception(f"input column count {column_count} is not match with the schema count {schema_columns_count}")
        
        return is_column_match         
    
    def __check_column_names(self, df_input: pd.DataFrame)  ->bool:
        
        is_column_name_match = False
        schema_column_name = list(self.model_schema_info["columns"].keys())
        input_columns_name = list(df_input.columns)
        
        if collections.Counter(schema_column_name) == collections.Counter(input_columns_name):
            is_column_name_match = True
        else:
            raise Exception(f"feature name mismatch between schema {schema_column_name} and input {input_columns_name} ")
        
        return is_column_name_match
        
    
    def __get_train_test_data(self):
        
        train_df = pd.read_csv(self.data_ingestion_artifact.ingected_train_file_path)
        test_df = pd.read_csv(self.data_ingestion_artifact.ingected_test_file_path)
        
        return train_df, test_df
    
    def __validate_data_set_schema(self)-> bool:
        
        validation_status = False
        
        train_df, test_df = self.__get_train_test_data()
        
        # check number of columns in the test and train dataset 
        self.__check_number_of_columns(train_df)
        self.__check_number_of_columns(test_df)
        
        # check columsn names
        self.__check_column_names(train_df)
        self.__check_column_names(test_df)
        
        return validation_status
    
    def __save_data_drift_report(self):
        
        profile = Profile(sections=[DataDriftProfileSection()])
        train_df,test_df = self.__get_train_test_data()
        profile.calculate(train_df,test_df)
        report = json.loads(profile.json())

        report_file_path = self.data_validation_artifact.report_file_path
        # report_dir = os.path.dirname(report_file_path)
        # os.makedirs(report_dir,exist_ok=True)
        with open(report_file_path,"w") as report_file:
            json.dump(report, report_file, indent=6)
            
        return report
    
    def __save_data_drift_report_page(self):
        dashboard = Dashboard(tabs=[DataDriftTab()])
        train_df,test_df = self.__get_train_test_data()
        dashboard.calculate(train_df,test_df)
        report_page_file_path = self.data_validation_artifact.report_page_file_path
        # report_page_dir = os.path.dirname(report_page_file_path)
        # os.makedirs(report_page_dir,exist_ok=True)

        dashboard.save(report_page_file_path)   
    
    def __is_data_drift_found(self):
        """
            Used to found the data drift, We will be using evidently to check the data drift
            Here we will be cheking the data drift between test and train data. 
            In actual, we can use it to check the data drift between the old and new dataset 
        """
        report = self.__save_data_drift_report()
        self.__save_data_drift_report_page()
        
        if report['data_drift']['data']['metrics']['dataset_drift'] == True:
            raise Exception("data drift found")
        
        logger.info("No data drift found")
        return True
        
    
    def start_data_data_validation(self):
        self.__is_train_test_file_exists()
        self.__validate_data_set_schema()
        self.__is_data_drift_found()