import json
from typing import Dict, List

# Ruta del archivo JSON que almacenará los contextos de usuario
CONTEXT_FILE = 'user_contexts.json'

# Función para cargar los contextos desde el archivo JSON
def load_contexts() -> Dict[str, List[str]]:
    try:
        with open(CONTEXT_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Función para guardar los contextos en el archivo JSON
def save_contexts(contexts: Dict[str, List[str]]):
    with open(CONTEXT_FILE, 'w') as file:
        json.dump(contexts, file, indent=4)

# Función para obtener el contexto de un usuario
def get_user_context(user_id: str) -> List[str]:
    contexts = load_contexts()
    if user_id not in contexts:
        contexts[user_id] = ["Te llamas Inés y te tienes que comportar como una empleada de recursos humanos que vas a hacer una entrevista de trabajo para el puesto de desarrollador web"]
    return contexts[user_id]

# Función para actualizar el contexto de un usuario
def update_user_context(user_id: str, message: str):
    contexts = load_contexts()
    if user_id not in contexts:
        contexts[user_id] = []
    contexts[user_id].append(message)
    # Limitar el contexto a las últimas 10 interacciones para evitar sobrecarga
    contexts[user_id] = contexts[user_id][-10:]
    save_contexts(contexts)

# Función para reiniciar el contexto de un usuario
def reset_user_context(user_id: str):
    contexts = load_contexts()
    contexts[user_id] = ["Te llamas Inés y te tienes que comportar como una empleada de recursos humanos que vas a hacer una entrevista de trabajo para el puesto de desarrollador web"]
    save_contexts(contexts)