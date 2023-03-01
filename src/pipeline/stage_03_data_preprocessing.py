from src import logger
from src.config.configuration import ConfigurationManager
from src.components.data_preprocessing import DataPreprocessing

STAGE_NAME = "Data preprocessing stage"

def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_configuration()
    data_preprocessing_config = config.get_data_preprocessing_configuration()
    
    data_proprocessing = DataPreprocessing(data_ingestion_config=data_ingestion_config, 
                                           data_preprocessing_config=data_preprocessing_config)
    
    data_proprocessing.start_data_preprocessing()

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<< \n==============")
    except Exception as e:
        logger.exception(e)
        raise e
