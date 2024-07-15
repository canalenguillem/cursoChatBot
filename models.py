from pydantic import BaseModel, Field

class Message(BaseModel):
    text: str = Field(..., example="¿Cuál es la capital de Francia?")

class ChatResponse(BaseModel):
    response: str
    audio_url: str