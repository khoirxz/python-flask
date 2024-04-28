# app/models/prediksi.py

import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

def get_result(start_day, days, selected_model):
    """Get result predict"""

    basefolder = os.path.join(os.getcwd(), "app", "models", "data")

    model1 = pickle.load(open(basefolder + "\\LR1.pkcls", "rb"))
    model2 = pickle.load(open(basefolder + "\\LR2.pkcls", "rb"))
    model3 = pickle.load(open(basefolder + "\\LR3.pkcls", "rb"))

    if selected_model == "1":
        models = [("Model 1", model1)]
    elif selected_model == "2":
        models = [("Model 2", model2)]
    elif selected_model == "3":
        models = [("Model 3", model3)]
    elif selected_model == "all":
        models = [("Model 1", model1), ("Model 2", model2), ("Model 3", model3)]
    else:
        models = [("Model 1", model1)]  # Default to Model 1 if invalid option selected

    predictions = {model_name: [] for model_name, _ in models}
    total_predictions = {model_name: 0 for model_name, _ in models}

    for day_number in range(start_day, start_day + days):
        for model_name, model in models:
            prediction = model.predict([[day_number]])
            rounded_prediction = round(float(prediction), 2)
            total_predictions[model_name] += rounded_prediction
            predictions[model_name].append((day_number, rounded_prediction))

    grand_total_prediction = sum(total_predictions.values()) / len(models)  # Hitung total prediksi dari semua model

    average_total_prediction = grand_total_prediction / len(models)  # Hitung rata-rata total prediksi

    for model_name in predictions:
        total_predictions[model_name] = round(total_predictions[model_name] / days, 2)
    return predictions, total_predictions, grand_total_prediction, average_total_prediction



