import json
import re
from unidecode import unidecode

def create_inverse_synonyms(synonyms_map):
    inverse_map = {}
    for base_word, variants in synonyms_map.items():
        inverse_map[base_word] = base_word
        for variant in variants:
            inverse_map[variant] = base_word
    return inverse_map

def load_info(path='info.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        respuestas = datos['respuestas']
        reglas = datos['reglas']
        sinonimos_inversos = create_inverse_synonyms(datos.get('sinonimos', {}))
        respuestas_avanzadas = datos.get("respuestas_avanzadas", {})
        return respuestas, reglas, sinonimos_inversos, respuestas_avanzadas
    except FileNotFoundError:
        raise
    except json.JSONDecodeError:
        raise
    except KeyError as e:
        raise

def save_info(data, path='info.json'):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)