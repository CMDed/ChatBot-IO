import re
from unidecode import unidecode
# ------------------------------------------
# Chatbot Educativo: Mentor Funcional
# ------------------------------------------

# No ejecuta nada por sí misma, solo "describe" qué se debe hacer.
class IOAction:
    def __init__(self, kind, value=None):
        self.kind = kind  # Tipo de acción: "Input" o "Output"
        self.value = value  # Contenido de la acción


# No imprime, no lee ni modifica nada externo, es completamente pura.
def process_message(message):

    message = unidecode(message.lower())
    message = re.sub(r'[^\w\s]', '', message)

    responses = {
        "funcion pura": "Una función pura siempre devuelve el mismo resultado si los argumentos son iguales y no causa efectos secundarios.",
        "monada": "Una mónada es una estructura que permite encadenar operaciones con efectos controlados.",
        "io": "En programación funcional, IO representa operaciones de entrada/salida que se controlan de forma segura.",
        "efectos secundarios": "Un efecto secundario ocurre cuando una función modifica algo fuera de su ámbito o depende del estado externo."
    }

    key = next((k for k in responses if k in message), None)

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
        # Leer mensaje del usuario (efecto controlado)
        message = interpret(IOAction("Input"))

        # Condición de salida
        if message.lower() == "salir":
            print("Hasta luego.")
            break

        # Procesar el mensaje (parte pura)
        action = process_message(message)

        # Ejecutar la acción (efecto controlado)
        interpret(action)


# Punto de entrada del programa
if __name__ == "__main__":
    main()