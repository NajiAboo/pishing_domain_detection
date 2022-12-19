from src.util import read_yaml, create_directories
from src.entity import DataIngestionConfig, DataValidationConfig
from src.constants import PARAMS_FILE_PATH
import os

class ConfigurationManager:
    def __init__(self, params_file_path = PARAMS_FILE_PATH ) -> None:
        self.params = read_yaml(params_file_path)
    
    def get_data_ingestion_configuration(self) -> DataIngestionConfig:
        config = self.params.data_ingestion
        
        create_directories([config.root_dir,  
                            os.path.dirname(config.local_data_file),
                            os.path.dirname(config.ingected_test_file_path),
                            os.path.dirname(config.ingected_train_file_path)
                            ])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir= config.root_dir,
            source_URL= config.source_URL, 
            local_data_file= config.local_data_file, 
            unzip_dir= config.unzip_dir,
            ingected_test_file_path=config.ingected_test_file_path,
            ingected_train_file_path=config.ingected_train_file_path
        )
        
        return data_ingestion_config
    
    def get_data_validation_configuration(self) -> DataValidationConfig:
        config = self.params.data_validation
        
        create_directories([config.root_dir,
                            os.path.dirname(config.report_file_path),
                            os.path.dirname(config.report_page_file_path)
                            ])
        
        data_valiation_config = DataValidationConfig(
            root_dir=config.root_dir, 
            schema_path_file= config.schema_path_file, 
            report_file_path=config.report_file_path,
            report_page_file_path=config.report_page_file_path
        )
        
        return data_valiation_config