from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["dataset_download_url", "ingested_dir", "raw_data_dir"])


DataValidationConfig = namedtuple("DataValidationConfig", ["clean_data_dir", "serialized_objects_dir", "books_csv_file", "ratings_csv_file"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["clean_data_file_path", "transformed_data_dir"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["transformed_data_dir","trained_model_dir", "trained_model_name"])