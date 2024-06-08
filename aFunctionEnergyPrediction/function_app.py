import azure.functions as func
import logging
import pickle
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="aFunctionEnergyPrediction")
def aFunctionEnergyPrediction(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Starting prediction ....')


    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:

        Lagging_Current_Reactive_Power_KvarH = req_body.get('Lagging_Current_Reactive_Power_KvarH')
        Leading_Current_Reactive_Power_kVarh = req.body.get('Leading_Current_Reactive_Power_kVarh')
        CO2_tCo2 = req.body.get('CO2_tCo2')
        logging_Current_Power_Factor = req.body.get('logging_Current_Power_Factor')
        Leading_Current_Power_Factor = req.body.get('Leading_Current_Power_Factor')
        NSM = req.body.get('NSM')
        WeekStatus = req.body.get(WeekStatus)
        Day_of_week = req.body.get('Day_of_week')
        Load_Type = req.body.get('Load_Type')        
    
        X_test = [Lagging_Current_Reactive_Power_KvarH, Leading_Current_Reactive_Power_kVarh, CO2_tCo2, logging_Current_Power_Factor, Leading_Current_Power_Factor, NSM, WeekStatus, Day_of_week, Load_Type]

        # Loading model 
        
        model_pkl_file = "./energyPredictorModel.pkl"
                
        with open(model_pkl_file, 'rb') as file : 
            model = pickle.load(file)   
        
        Usage_Kw =  model.predict([X_test])
        logging.info(f"Usage_Kw : {Usage_Kw}")
        return func.HttpResponse(str(Usage_Kw), status_code=200)

    