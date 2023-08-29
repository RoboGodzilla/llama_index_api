from fastapi import FastAPI
from typing import Callable

from app.utils import construct_index


def create_start_app_handler() -> Callable:
    def start_app() -> None:
        pass

    return start_app