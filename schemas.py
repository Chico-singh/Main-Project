from pydantic import BaseModel

class ExpenseData(BaseModel):

    category:int

    account:int

    currency:int

    tags:int

    Year:int

    Month:int

    Day:int

    Weekday:int

    Weekend:int

    Quarter:int