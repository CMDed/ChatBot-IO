import pytest
from core import (
    normalize_message,
    expand_synonyms,
    remove_stopwords,
    rebuild_text,
    detect_first_match
)

def test_normalize_message():
    text = "¡Hólá, Función Púra!"
    assert normalize_message(text) == "hola funcion pura"

def test_expand_synonyms():
    words = ["funciones", "puras"]
    sinonimos = {"funciones": "funcion", "puras": "pura"}
    result = expand_synonyms(words, sinonimos)
    assert result == ["funcion", "pura"]

def test_remove_stopwords():
    words = ["que", "es", "funcion", "pura"]
    result = remove_stopwords(words)
    assert result == ["funcion", "pura"]

def test_rebuild_text():
    words = ["funcion", "pura"]
    result = rebuild_text(words)
    assert result == "funcion pura"

def test_detect_first_match():
    reglas = [
        (r"\bfuncion pura\b", "funcion pura"),
        (r"\bmonada\b", "monada")
    ]
    message = "esto es una funcion pura"
    assert detect_first_match(message, reglas) == "funcion pura"