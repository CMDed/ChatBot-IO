import re
from unidecode import unidecode
from functools import reduce

#No ejecuta nada por sí misma, solo "describe" qué se debe hacer
class IOAction:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

def get_respuesta(topic):
    if topic == "funcion pura":
        return "Una función pura siempre devuelve el mismo resultado si los argumentos son iguales y no causa efectos secundarios."
    elif topic == "monada":
        return "Una mónada es una estructura que permite encadenar operaciones con efectos controlados."
    elif topic == "io":
        return "En programación funcional, IO representa operaciones de entrada/salida que se controlan de forma segura."
    elif topic == "efecto secundario":
        return "Un efecto secundario ocurre cuando una función modifica algo fuera de su ámbito o depende del estado externo."
    elif topic == "saludo":
        return "Hola, soy tu mentor del curso de Lenguajes de Programación. Puedo explicarte sobre programación funcional, ¿alguna pregunta?"
    else:
        return "Puedo explicarte sobre funciones puras, mónadas, IO o efectos secundarios."
    
#tuplas
reglas=[
    (r'\bfuncion pura\b', "funcion pura"),
    (r'\bmonada\b', "monada"),
    (r'\bio\b', "io"),
    (r'\befecto secundario\b', "efecto secundario"),
    (r'\b(hola|saludo)\b', "saludo"),
]

#No imprime, no lee ni modifica nada externo, es completamente pura
def process_message(message):
    # Normalización básica
    message = unidecode(message.lower())
    message = re.sub(r'[^\w\s]', '', message)
    
    #pipeline funcional
    words = message.split()
    stopwords = ["que", "es", "son", "los", "las", "un", "una", "de", "en", "y", "sobre", "acerca"]
    
    #sinónimo
    synonyms = {
        "funciones": "funcion",
        "puras": "pura",
        "puro": "pura",
        "monadas": "monada",
        "monad": "monada",
        "io": "io",
        "entrada": "io",
        "salida": "io",
        "efectos": "efecto",
        "secundarios": "secundario",
        "colaterales": "secundario",
        "saludos": "saludo"
    }

    #normalizar palabras
    words = list(map(lambda w: synonyms[w] if w in synonyms else w, words))
    
    #eliminar stopwords
    words = list(filter(lambda w: w not in stopwords, words))
    
    #reconstruir texto procesado
    message = reduce(lambda acc, w: acc + " " + w, words, "").strip()

    coincidencia = next(
        (topic for pattern, topic in reglas if re.search(pattern, message)),
        None
    )

    if coincidencia:
        response_text = get_respuesta(coincidencia)
    else:
        response_text = "Reformula la respuesta, puedo explicarte sobre funciones puras, mónadas, IO o efectos secundarios."
    return IOAction("Output", response_text)

#intérprete
def interpret(action):
    if action.kind == "Output":
        print(f"Mentor Funcional: {action.value}")
    elif action.kind == "Input":
        return input("Tú: ")


#main
def main():
    print("Bienvenido a Mentor Funcional. Escribe 'salir' para terminar.\n")

    while True:

        message = interpret(IOAction("Input"))

        if message.lower() == "salir":
            print("Hasta luego.")
            break

        action = process_message(message)

        interpret(action)


#punto de entrada
if __name__ == "__main__":
    main()