from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils import (
    chatbot_generator
)


router = APIRouter()

class PrompData(BaseModel):
    question: str

@router.post("/gen_answer")
async def generate_answer(body: PrompData):
    query = chatbot_generator(body.question)

    return JSONResponse(
        content= query,
        status_code=200
    )