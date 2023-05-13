from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from gtts import gTTS
from speech_recognition import (
    Recognizer,
    AudioFile,
    UnknownValueError
)
import uuid

def convert_text_2_speech(text: str):
    speech_engine = gTTS(
        text=text,
        lang='es',
        slow=False,
        tld="com.mx"
    )
    filename = "{}.wav".format(str(uuid.uuid4().hex))
    speech_engine.save("app/media/" + filename)
    return filename


def convert_speech_2_text(audio_file: str):
    
    r = Recognizer()

    with AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio)

    except UnknownValueError as e:
        return e