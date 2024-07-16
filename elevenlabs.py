import os
import requests
from decouple import config

# Cargar la clave API desde el archivo .env
ELEVENLABS_API_KEY = config('ELEVENLABS_API_KEY')

def convert_text_to_speech(message,output_file="output.mp3"):
    print("try convert to speech")
    body = {
    "text": message,
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
        }
    }

    #define voice
    voice_rachel="21m00Tcm4TlvDq8ikWAM"
    
    headers = { "xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"
    
    try:
        print("--------------try request post")
        response=requests.post(endpoint,json=body,headers=headers)

        # Guardar la respuesta de audio en un archivo
        with open(output_file, 'wb') as f:
            f.write(response.content)
    
    except Exception as e:
        print(f"request error {e}")
        
    #handle response
    if response.status_code==200:
        return response.content
    else:
        print(f"status_code {response.status_code}")
        return

def text_to_speech(text: str, output_file: str = "output.mp3") -> str:
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        print("before request")
        response = requests.post(
            url,
            headers=headers,
            json=data
        )
        print(f"after request {response}")
        response.raise_for_status()

        # Guardar la respuesta de audio en un archivo
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        # Devolver la ruta completa del archivo guardado
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    response = convert_text_to_speech("my name is will")
    # Guardar la respuesta de audio en un archivo
    print(response)
    with open("outputrwa.mp3", 'wb') as f:
        f.write(response)
