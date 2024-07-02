from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_subscribed_user
from app.log import get_logger
from app.models.user import User
from app.schemas.macros import Macros

macros_router = APIRouter()

log = get_logger(__name__)


@macros_router.get(
    "", status_code=status.HTTP_200_OK, summary="Get current user macros", response_model=Macros
)
async def macros(user: Annotated[User, Depends(get_current_subscribed_user)]):
    weight = user.weight
    if not weight:
        log.info("macros: user weight is not set")
        raise HTTPException(status_code=400, detail="User weight is not set")
    calories = weight * 33
    proteins = round(weight * 1.7)
    fats = round(max(weight * 0.8, 50))
    carbohydrates = round((calories - (proteins * 4 + fats * 9)) / 4)
    log.info("macros: macros have been received")
    return Macros(
        calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates
    )


