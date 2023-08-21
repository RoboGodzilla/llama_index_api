import os
import shutil
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils import (
    construct_index,
    chatbot_generator
)


router = APIRouter()

# user uploads multiple files to a directory
@router.post("/uploadfile/")
async def create_upload_file(directory_path: str, files: list[UploadFile]):
    if directory_path == "":
        return JSONResponse(
            status_code=400,
            content= "Please specify a directory path"
        )
    if not os.path.exists("docs/"+directory_path):
        os.makedirs("docs/"+directory_path)

    for file in files:
        with open("docs/"+directory_path+"/"+file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    construct_index(directory_path)

    return JSONResponse(
        status_code=200,
        content= "File uploaded successfully"
    )

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