import re
from unidecode import unidecode
from functools import reduce

# No ejecuta nada por sí misma, solo "describe" qué se debe hacer.
class IOAction:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

# No imprime, no lee ni modifica nada externo, es completamente pura.
def process_message(message):
    message = unidecode(message.lower())
    message = re.sub(r'[^\w\s]', '', message)
    
    #pipeline funcional
    words = message.split()
    stopwords = ["que", "es", "son", "los", "las", "un", "una", "de", "en", "y"]
    
    #normalizar palabras
    words = list(map(lambda w: w.strip(), words))
    
    #eliminar stopwords
    words = list(filter(lambda w: w not in stopwords, words))
    
    #reconstruir texto procesado
    message = reduce(lambda acc, w: acc + " " + w, words, "").strip()

    responses = {
        "funcion pura": "Una función pura siempre devuelve el mismo resultado si los argumentos son iguales y no causa efectos secundarios.",
        "funciones puras": "Una función pura siempre devuelve el mismo resultado si los argumentos son iguales y no causa efectos secundarios.",
        "monada": "Una mónada es una estructura que permite encadenar operaciones con efectos controlados.",
        "monadas": "Una mónada es una estructura que permite encadenar operaciones con efectos controlados.",
        "io": "En programación funcional, IO representa operaciones de entrada/salida que se controlan de forma segura.",
        "efecto secundario": "Un efecto secundario ocurre cuando una función modifica algo fuera de su ámbito o depende del estado externo.",
        "efectos secundarios": "Un efecto secundario ocurre cuando una función modifica algo fuera de su ámbito o depende del estado externo."
    }

    key = next((k for k in responses if re.search(rf'\b{k}\b', message)), None)
    if key:
        return IOAction("Output", responses[key])
    else:
        return IOAction("Output", "Puedo explicarte sobre funciones puras, mónadas, IO o efectos secundarios.")

# Intérprete: ejecuta las acciones descritas (aquí sí hay efectos secundarios controlados)
def interpret(action):
    if action.kind == "Output":
        print(f"Mentor Funcional: {action.value}")
    elif action.kind == "Input":
        return input("Tú: ")


# Programa principal:conecta las piezas sin mezclar la lógica pura con los efectos
def main():
    print("Bienvenido a Mentor Funcional. Escribe 'salir' para terminar.\n")

    while True:

        message = interpret(IOAction("Input"))

        if message.lower() == "salir":
            print("Hasta luego.")
            break

        action = process_message(message)

        interpret(action)


# Punto de entrada del programa
if __name__ == "__main__":
    main()