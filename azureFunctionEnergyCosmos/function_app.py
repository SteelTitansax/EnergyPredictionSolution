import azure.functions as func
import logging
import pickle

app = func.FunctionApp()

@app.cosmos_db_trigger(arg_name="azcosmosdb", container_name="energy",database_name="energy", connection="energypredictioncosmosdb_DOCUMENTDB", LeaseContainerName = "leases",CreateLeaseContainerIfNotExists = True)  

def energyCosmos(azcosmosdb: func.DocumentList):
    logging.info('Python CosmosDB triggered.')
    if azcosmosdb:
        logging.info(f'Received {len(azcosmosdb)} documents')
        logging.info('Starting prediction ....')

        for doc in azcosmosdb:

            Lagging_Current_Reactive_Power_KvarH = doc.get('Lagging_Current_Reactive_Power_KvarH')
            Leading_Current_Reactive_Power_kVarh = doc.get('Leading_Current_Reactive_Power_kVarh')
            CO2_tCo2 = doc.get('CO2_tCo2')
            logging_Current_Power_Factor = doc.get('logging_Current_Power_Factor')
            Leading_Current_Power_Factor = doc.get('Leading_Current_Power_Factor')
            NSM = doc.get('NSM')
            WeekStatus = doc.get('WeekStatus')
            Day_of_week = doc.get('Day_of_week')
            Load_Type = doc.get('Load_Type')        
        
            X_test = [Lagging_Current_Reactive_Power_KvarH, Leading_Current_Reactive_Power_kVarh, CO2_tCo2, logging_Current_Power_Factor, Leading_Current_Power_Factor, NSM, WeekStatus, Day_of_week, Load_Type]

            # Loading model 
            
            model_pkl_file = "./energyPredictorModel.pkl"
                    
            with open(model_pkl_file, 'rb') as file : 
                model = pickle.load(file)   
            
            Usage_Kw =  model.predict([X_test])
            logging.info(f"Usage_Kw : {Usage_Kw}")
            logging.info("Prediction completed!!")
            return func.HttpResponse(str(Usage_Kw), status_code=200)