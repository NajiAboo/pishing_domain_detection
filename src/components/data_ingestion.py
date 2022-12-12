import os
import urllib.request as request
from src import logger
from pathlib import Path
from src.util import get_size
from src.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config
        
    def download_file(self):
        logger.info("Trying to download file ...")
        
        is_exist = os.path.exists(self.config.local_data_file)
        
        if not is_exist:
            logger.info("Started downloading")
            
            opener = request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            filename, headers = opener.retrieve(url=self.config.source_URL, 
                                                filename=self.config.local_data_file)
 
            logger.info(f"{filename} downloaded with following info {headers}")
            
        else:
            logger.info(f"File already exist of size {get_size(Path(self.config.local_data_file))}")
        
    