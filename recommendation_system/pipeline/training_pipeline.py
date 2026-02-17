from recommendation_system.components.stage_00_data_ingestion import DataIngestion

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()

    def start_data_ingestion(self):

        # Starts the training pipeline: returns None
        
        self.data_ingestion.initiate_data_ingestion()
