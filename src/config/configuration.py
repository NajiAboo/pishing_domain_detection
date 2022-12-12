from src.util import read_yaml, create_directories
from src.entity import DataIngestionConfig
from src.constants import PARAMS_FILE_PATH
import os

class ConfigurationManager:
    def __init__(self, params_file_path = PARAMS_FILE_PATH ) -> None:
        self.params = read_yaml(params_file_path)
    
    def get_data_ingestion_configuration(self) -> DataIngestionConfig:
        config = self.params.data_ingestion
        
        create_directories([config.root_dir,  os.path.dirname(config.local_data_file)])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir= config.root_dir,
            source_URL= config.source_URL, 
            local_data_file= config.local_data_file, 
            unzip_dir= config.unzip_dir
        )
        
        return data_ingestion_config
    