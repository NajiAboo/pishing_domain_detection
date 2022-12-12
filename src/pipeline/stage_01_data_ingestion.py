
from src.config import ConfigurationManager
from src.components import DataIngestion
from src import logger

STAGE_NAME = "Data Ingestion stage"

def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_configuration()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion.download_file()
    
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<< \n==============")
    except Exception as e:
        logger.exception(e)
        raise e