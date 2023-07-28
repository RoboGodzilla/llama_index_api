import uvicorn
from fastapi import FastAPI

from app.create_app import create_app

app = create_app()

if __name__ == "__main__":

    uvicorn.run(
        app="main:app",
        port=5000,
    )
