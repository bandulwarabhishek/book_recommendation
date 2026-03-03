import os
import sys
import pickle
import pandas as pd
from recommendation_system.logger.log import logging
from recommendation_system.config.configuration import AppConfiguration
from recommendation_system.exception.exception_handler import AppException
from sklearn.neighbors import NearestNeighbors
from recommendation_system.entity.config_entity import ModelTrainerConfig
from scipy.sparse import csr_matrix

class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e
        

    def train(self):
        try:
            #loading pivot data
            book_pivot = pickle.load(open(os.path.join(self.model_trainer_config.transformed_data_dir,"transformed_data.pkl"),'rb'))
            book_sparse = csr_matrix(book_pivot)
            #Training model
            model = NearestNeighbors(algorithm='brute')
            model.fit(book_sparse)
            #saving model object for recommendation
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            file_name = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name)
            pickle.dump(model, open(file_name,'wb'))
            logging.info(f"Saved trained model to {file_name}")

        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def initiate_model_trainer(self):
        try:
            logging.info(f"{'='*20}Model Trainer log started.{'='*20} ")
            self.train()
            logging.info(f"{'='*20}Model Trainer log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e