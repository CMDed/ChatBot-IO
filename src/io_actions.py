class IOAction:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

def interpret(action):
    """Interpreta una acción IOAction en la consola."""
    if action.kind == "Output":
        print(f"MentorCORE: {action.value}")
    elif action.kind == "Input":
        return input("Tú: ")
    elif action.kind == "Log":
        print(f"[LOG]: {action.value}")
    elif action.kind == "LogIntent":
        from analytics import log_intent
        log_intent(action.value)
        print(f"[LOG]: Intención registrada: {action.value}")
    elif action.kind == "ShowStats":
        print(action.value)
    else:
        print(f"[UNKNOWN ACTION]: {action.kind} -> {action.value}")