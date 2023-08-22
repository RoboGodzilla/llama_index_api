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
@router.post("/uploadfiles")
async def create_upload_file( files: list[UploadFile], directory_path: str = "" ):
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
    document: str

@router.post("/api/answer")
async def generate_answer(body: PrompData):
    query = chatbot_generator(body.question, body.prompt, body.document)

    return JSONResponse(
        content= query,
        status_code=200
    )