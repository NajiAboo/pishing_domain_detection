from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    ingected_train_file_path: Path
    ingected_test_file_path: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    schema_path_file: Path
    report_file_path: Path
    report_page_file_path: Path

@dataclass(frozen=True)
class DataPreprcessingConfig:
    root_dir: Path
    elbow_file_path: Path
    cluster_number_path: Path
    clustered_data: Path
    cluster_model_path: Path
    