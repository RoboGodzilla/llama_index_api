import os
import shutil
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils import (
    construct_index,
    chatbot_generator
)


router = APIRouter()

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

class PrompData(BaseModel):
    question: str
    prompt: str

@router.post("/api/answer")
async def generate_answer(body: PrompData):
    query = chatbot_generator(body.question, body.prompt)

    return JSONResponse(
        content= query,
        status_code=200
    )