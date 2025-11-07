import re
from unidecode import unidecode
from functools import reduce
import json

#No ejecuta nada por sí misma, solo "describe" qué se debe hacer
class IOAction:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

def create_inverse_synonyms(synonyms_map):
    inverse_map = {}
    for base_word, variants in synonyms_map.items():
        inverse_map[base_word] = base_word
        for variant in variants:
            inverse_map[variant] = base_word
    return inverse_map

#No imprime, no lee ni modifica nada externo, es completamente pura
def process_message(message, reglas, respuestas, sinonimos_inversos):
    # Normalización básica
    message = unidecode(message.lower())
    message = re.sub(r'[^\w\s]', '', message)
    
    #pipeline funcional
    words = message.split()
    stopwords = ["que", "es", "son", "los", "las", "un", "una", "de", "en", "y", "sobre", "acerca"]
    
    # normalizar
    words = list(map(
        lambda w: sinonimos_inversos.get(w, w),
        words
    ))
    
    # eliminar
    words = list(filter(lambda w: w not in stopwords, words))
    
    # reconstruir
    message = reduce(lambda acc, w: acc + " " + w, words, "").strip()

    coincidencia = next(
        (topic for pattern, topic in reglas if re.search(pattern, message)),
        None
    )

    if coincidencia:
        response_text = respuestas.get(coincidencia)
    else:
        response_text = respuestas.get('fallback', "Reformula la respuesta, puedo explicarte sobre funciones puras, mónadas, IO o efectos secundarios.")
        
    return [
        IOAction("Log", f"Intención detectada: {coincidencia or 'No encontrado'}"),
        IOAction("Output", response_text)
    ]

#intérprete
def interpret(action):
    if action.kind == "Output":
        print(f"MentorCORE: {action.value}")
    elif action.kind == "Input":
        return input("Tú: ")
    elif action.kind == "Log":
        print(f"[LOG]: {action.value}")

#main
def main():
    print("Bienvenido a MentorCORE. Escribe 'salir' para terminar.\n")

    try:
        with open('info.json', 'r', encoding='utf-8') as f:
            datos_modelo = json.load(f)
        respuestas = datos_modelo['respuestas']
        reglas = datos_modelo['reglas']
        
        sinonimos_inversos = create_inverse_synonyms(datos_modelo['sinonimos'])
        
    except FileNotFoundError:
        print("Error: No se encontró 'info.json'. Deteniendo programa.")
        return
    except json.JSONDecodeError:
        print("Error: El archivo 'info.json' tiene un formato incorrecto. Deteniendo programa.")
        return
    except KeyError as e:
        print(f"Error: Falta la clave {e} en 'info.json'. Deteniendo programa.")
        return

    while True:

        message = interpret(IOAction("Input"))

        if message.lower() == "salir":
            print("Hasta luego.")
            break
        
        actions = process_message(message, reglas, respuestas, sinonimos_inversos)

        for action in actions:
            interpret(action)


#punto de entrada
if __name__ == "__main__":
    main()