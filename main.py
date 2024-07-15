from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse,StreamingResponse

from pydantic import BaseModel
from chatgpt import get_chatgpt_response
from elevenlabs import convert_text_to_speech
import os
app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat/")
def chat(message: Message):
    user_input = message.text
    response_text = get_chatgpt_response(user_input)
    if response_text.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response_text)

    # Convert chat response to audio
    audio_output = convert_text_to_speech(response_text)
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
    
