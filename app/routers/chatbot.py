from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uuid
import io

from app.utils import (
    chatbot_generator,
    convert_text_2_speech,
    convert_speech_2_text
)


router = APIRouter()

class PrompData(BaseModel):
    promp: str
    generate_audio: bool = False


class AudioData(BaseModel):
    name: str


@router.post("/generate_answer")
async def generate_answer(body: PrompData):
    answer = chatbot_generator(body.promp)
    audio_file = None

    if body.generate_audio:
        audio_file = convert_text_2_speech(answer)

    return JSONResponse(
        content={
            "answer": answer.replace("\n", ""),
            "audio_file": audio_file,
        },
        status_code=200
    )


@router.post("/dictated")
async def voice_dictated(audio_input: UploadFile = Form(...)):
    
    filename = "{}.wav".format(str(uuid.uuid4().hex))
    file_dir = "app/media/" + filename

    # read the file
    with open(file_dir, "wb") as buffer:
        buffer.write(audio_input.file.read())

    return JSONResponse(
        content={"response": convert_speech_2_text(file_dir)},
        status_code=200
    )


@router.post("/audio")
async def get_audio(audio_input: AudioData):

    # def stream_audio():
    #     with io.BytesIO("app/media/" + audio_input.name) as audio_file:
    #         while True:
    #             chunk = audio_file.read(1024)
    #             if not chunk:
    #                 break
    #             yield chunk

    with open("app/media/" + audio_input.name, "rb") as audio_file:
        # Create a BytesIO object and write the audio file to it
        audio_stream = io.BytesIO(audio_file.read())

    headers = {
        "Content-Type": "audio/wav"
    }
    return StreamingResponse(audio_stream, headers=headers)