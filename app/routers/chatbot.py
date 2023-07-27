from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils import (
    chatbot_generator
)


router = APIRouter()

class PrompData(BaseModel):
    promp: str

@router.post("/gen_answer")
async def generate_answer(body: PrompData):
    answer = chatbot_generator(body.promp)

    return JSONResponse(
        content={
            "answer": answer,
        },
        status_code=200
    )