from fastapi import FastAPI
from predict import predict_expense
from schemas import ExpenseData

app = FastAPI(
    title="AI Personal Finance API",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message":"AI Personal Finance Expense Tracker API"
    }

@app.post("/predict")
def prediction(data: ExpenseData):

    result = predict_expense(data)

    return {
        "Predicted Expense": result
    }