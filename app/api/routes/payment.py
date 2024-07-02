import stripe
from fastapi import APIRouter, Depends, Request, responses

from app.api.dependencies import get_current_user
from app.dao.user import UserDAO
from app.database import db_dependency
from app.log import get_logger
from app.models.user import User

stripe_router = APIRouter()

log = get_logger(__name__)


@stripe_router.get("/checkout")
async def create_checkout_session(
    request: Request, user: User = Depends(get_current_user), price: int = 10
):
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": "price_1PXOuyBKxUP0XR6cqi29wPh9",
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url=str(request.base_url)
        + "/payment/success?session_id={CHECKOUT_SESSION_ID}",
        metadata={"user_id": user.id},
    )
    return responses.RedirectResponse(checkout_session.url)


@stripe_router.get("/success")
async def stripe_webhook(db: db_dependency, request: Request, session_id: str):
    session = stripe.checkout.Session.retrieve(session_id)

    user = int(session.metadata.get("user_id"))
    await UserDAO.update(db, user, is_subscribed=True)

    docs_url = request.url_for("swagger_ui_html")

    return responses.RedirectResponse(docs_url)
