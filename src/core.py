import re
from functools import reduce
from unidecode import unidecode

def normalize_message(message):
    message = unidecode(message.lower())
    message = re.sub(r'[^\w\s]', '', message)
    return message

def expand_synonyms(words, synonyms_map):
    return list(map(lambda w: synonyms_map.get(w, w), words))

def remove_stopwords(words, stopwords=None):
    if stopwords is None:
        stopwords = ["que", "es", "son", "los", "las", "un", "una", "de", "en", "y", "sobre", "acerca"]
    return list(filter(lambda w: w not in stopwords, words))

def rebuild_text(words):
    return reduce(lambda acc, w: acc + " " + w, words, "").strip()

def pipeline(*funcs):
    """Devuelve una función que aplica funcs en secuencia a un valor."""
    return lambda x: reduce(lambda acc, f: f(acc), funcs, x)

def detect_first_match(message, reglas):
    """Reglas: lista de [pattern, topic]. Retorna topic o None."""
    match = next((topic for pattern, topic in reglas if re.search(pattern, message)), None)
    return match

def process_message(message, reglas, respuestas, sinonimos_inversos):
    message_norm = normalize_message(message)
    words = message_norm.split()

    words = expand_synonyms(words, sinonimos_inversos)
    words = remove_stopwords(words)
    message_proc = rebuild_text(words)

    coincidencia = detect_first_match(message_proc, reglas)

    if coincidencia:
        response_text = respuestas.get(coincidencia)
    else:
        response_text = respuestas.get('fallback', "Reformula la respuesta, puedo explicarte sobre funciones puras, mónadas, IO o efectos secundarios.")
    return coincidencia, response_text