from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse,StreamingResponse

from pydantic import BaseModel
from chatgpt import get_chatgpt_response,transcribe_audio
from elevenlabs import text_to_speech
import os
from context import get_user_context, update_user_context, reset_user_context
import shutil

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat2/")
async def chat2(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a WAV or MP3 file.")

    temp_file_path = file.filename
    print(f" temp_file_path {temp_file_path}")
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    #Convert the audio file to MP3
    mp3_file_path = f"{os.path.splitext(temp_file_path)[0]}.mp3"

    try:
        print(f"mp3 file {mp3_file_path}")
        message_decoded=transcribe_audio(mp3_file_path)
        print(f"message decoded: {message_decoded}")
    except Exception as e:
        print(f"erro: {e}")

@app.post("/chat/")
async def chat(user_id: str, file: UploadFile = File(...)):
    try:
        
        # Save the file temporarily
        temp_file_path = file.filename
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Convert the audio file to MP3
        mp3_file_path = f"{os.path.splitext(temp_file_path)[0]}.mp3"
        transcription = transcribe_audio(mp3_file_path)
        if not transcription:
            raise HTTPException(status_code=500, detail=transcription)
        
        # Obtener el contexto del usuario
        context = get_user_context(user_id)
        context.append({"role": "user", "content": transcription})
        update_user_context(user_id, {"role": "user", "content": transcription})

        # Obtener respuesta de ChatGPT
        response_text = get_chatgpt_response(context)
        if not response_text:
            raise HTTPException(status_code=400, detail="Failed chat response")

        # Actualizar el contexto con la respuesta del chatbot
        update_user_context(user_id, {"role": "assistant", "content": response_text})

              

        print(f"response for eleven {response_text}")
        # Convert chat response to audio
        audio_output = text_to_speech(response_text)
        if not audio_output:
            raise HTTPException(status_code=400, detail="Failed audio output")

        # Create a generator that yields chunks of data
        def iterfile():
            yield audio_output

        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset_context/")
def reset_context(user_id: str):
    reset_user_context(user_id)
    return {"message": "Contexto reiniciado correctamente"}
    
