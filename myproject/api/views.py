from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import math
import os
import datetime
# Create your views here.
import pandas as pd
from prophet import Prophet
import json
import matplotlib.pyplot as plt
def model(dat):
    # Load the dataset
    db = {}

    # waste_dataset = ['waste.csv']
    for i in range(1,5):

        dataset = "waste" + str(i)
        current_directory = os.getcwd()
        data = pd.read_csv(
            current_directory+"\\api\\dataset\\{0}.csv".format(dataset))

        prophet_data = pd.DataFrame()
        prophet_data['ds'] = pd.to_datetime(data['ticket_date'])
        prophet_data['y'] = data['net_weight_kg']
        model = Prophet(interval_width=0.95)
        model.fit(prophet_data)

        # Generate future dates for prediction
        future_dates = model.make_future_dataframe(periods=3650)

        # Make predictions
        forecast = model.predict(future_dates)

        # storing in db
        start_2k23 = forecast[forecast['ds'] == '2023-01-01'].index[0]
        for i in range(start_2k23, len(forecast)):
            place_name = data['area'][0]
            if not place_name in db:
                db[place_name] = {}
            date = str([forecast.iloc[i]['ds']][0].date())
            db[place_name][date] = forecast.iloc[i]['yhat']
        # print("Solid Waste Generated " + str(db['Boralesgamuwa UC'][str(date.today())]))
    places = list(db.keys())
    res = {}
    for i in places:
        res[i]=[str(math.ceil(db[i][str(dat)] / 6000)),db[i][str(dat)]]
    return res



@api_view(['POST'])
def getData(request):

    data = request.data
    print(data)
    name = data["input"]
    dat = data["date"]
    res = model(dat)
    ans = res[name]
    # res = json.dumps(res)
    return Response({"data":ans})