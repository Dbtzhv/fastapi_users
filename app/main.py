import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api.routes.auth import auth_router
from app.api.routes.macros import macros_router
from app.api.routes.payment import stripe_router
from app.api.routes.user import user_router
from app.config import settings

app = FastAPI(title="Gym API", version="0.1.0")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(macros_router, prefix="/macros", tags=["Macros"])
app.include_router(stripe_router, prefix="/payment", tags=["Subscription"])


origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


stripe.api_key = settings.STRIPE_SECRET_KEY
