import joblib
import numpy as np

model = joblib.load("expense_model.pkl")

scaler = joblib.load("scaler.pkl")


def predict_expense(data):

    sample = np.array([[
        data.category,
        data.account,
        data.currency,
        data.tags,
        data.Year,
        data.Month,
        data.Day,
        data.Weekday,
        data.Weekend,
        data.Quarter
    ]])

    sample = scaler.transform(sample)

    prediction = model.predict(sample)

    return round(float(prediction[0]),2)