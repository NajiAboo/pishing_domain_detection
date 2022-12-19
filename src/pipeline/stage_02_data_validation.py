
from src.config import ConfigurationManager
from src.components import DataValidation
from src import logger

STAGE_NAME = "Data validation stage"

def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_configuration()
    data_validation_config = config.get_data_validation_configuration()
    
    data_validation = DataValidation(data_ingestion_config, data_validation_config)
    data_validation.start_data_data_validation()
      
    
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<< \n==============")
    except Exception as e:
        logger.exception(e)
        raise e