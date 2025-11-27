from core import process_message

def test_process_message_intent_found():
    reglas = [
        (r"\bfuncion pura\b", "funcion pura"),
        (r"\bmonada\b", "monada")
    ]

    respuestas = {
        "funcion pura": "Definición de función pura",
        "fallback": "No entendí"
    }

    sinonimos = {"funcion": "funcion", "pura": "pura"}

    intent, response = process_message("explicame funcion pura", reglas, respuestas, sinonimos)

    assert intent == "funcion pura"
    assert response == "Definición de función pura"

def test_process_message_no_intent():
    reglas = [(r"\bmonada\b", "monada")]
    respuestas = {"fallback": "No entendí"}
    sinonimos = {}
    intent, response = process_message("hola como estas", reglas, respuestas, sinonimos)
    assert intent is None
    assert response == "No entendí"