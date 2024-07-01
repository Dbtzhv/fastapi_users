from pydantic import BaseModel


class Macros(BaseModel):
    calories: int
    proteins: int
    fats: int
    carbohydrates: int
