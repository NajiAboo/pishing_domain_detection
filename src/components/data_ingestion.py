import os
import pandas as pd
import urllib.request as request
from src import logger
from pathlib import Path
from src.util import get_size
from src.entity import DataIngestionConfig
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config
        
    def __download_file(self):
        logger.info("Trying to download file ...")
        
        is_exist = os.path.exists(self.config.local_data_file)
        print(is_exist)
         
        if not is_exist:
            logger.info("Started downloading")
            
            opener = request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            filename, headers = opener.retrieve(url=self.config.source_URL, 
                                                filename=self.config.local_data_file)
 
            logger.info(f"{filename} downloaded with following info {headers}")
            
        else:
            logger.info(f"File already exist of size {get_size(Path(self.config.local_data_file))}")
        
    def __split_data_as_train_test(self):
        row_df = pd.read_csv(self.config.local_data_file)
        train, test = train_test_split(row_df, test_size=0.2, stratify=row_df["phishing"])
        
        if train is not None:
            train_file_path = os.path.join(self.config.ingected_train_file_path)
            train.to_csv(train_file_path,index=False)
        
        if test is not None:
            test_file_path = os.path.join(self.config.ingected_test_file_path)
            test.to_csv(test_file_path, index=False)
    
    def start_data_ingestion(self):
        self.__download_file()
        self.__split_data_as_train_test()
        
        