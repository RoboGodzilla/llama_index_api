from fastapi import FastAPI

from app.routers import chatbot
from .utils import construct_index
from .events import create_start_app_handler

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(chatbot.router)

    app.add_event_handler("startup", create_start_app_handler())

    return app