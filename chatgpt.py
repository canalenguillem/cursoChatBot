from openai import OpenAI
from decouple import config

# Cargar la clave API desde el archivo .env
api_key = config('OPENAI_API_KEY')

# Crear el cliente de OpenAI
client = OpenAI(api_key=api_key)

def get_chatgpt_response(messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        chatbot_response = response.choices[0].message.content.strip()
        return chatbot_response
    except Exception as e:
        return f"Error: {str(e)}"
    

def transcribe_audio(file_path):
    client = OpenAI()

    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text



# Ejemplo de uso
if __name__ == "__main__":
    user_input = "hola me llamo guillem y quiero aprender python"
    text=transcribe_audio("guillem.mp3")
    print(f"text: {text}")
