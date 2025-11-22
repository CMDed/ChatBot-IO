from data_loader import load_info
from core import process_message
from io_actions import IOAction, interpret
from analytics import compute_stats_and_plot

def main():
    print("Bienvenido a MentorCORE. Escribe 'salir' para terminar.\n")

    try:
        respuestas, reglas, sinonimos_inversos = load_info('info.json')
    except FileNotFoundError:
        print("Error: No se encontró 'info.json'. Deteniendo programa.")
        return
    except Exception as e:
        print(f"Error al cargar info.json: {e}")
        return

    while True:
        message = interpret(IOAction("Input"))
        if message is None:
            continue

        if message.lower() == "salir":
            print("Hasta luego.")
            break

        #comando para estadistica
        if message.strip().lower() in ["estadisticas", "estadísticas", "stats"]:
            res = compute_stats_and_plot()
            if res["plot"]:
                interpret(IOAction("Output", f"Resumen de intenciones:\n{res['message']}"))
                interpret(IOAction("Output", f"Gráfico guardado en: {res['plot']}"))
            else:
                interpret(IOAction("Output", res["message"]))
            continue

        coincidencia, response_text = process_message(message, reglas, respuestas, sinonimos_inversos)

        #registro de intecion
        interpret(IOAction("LogIntent", coincidencia))

        #registro de respuesta
        interpret(IOAction("Output", response_text))

if __name__ == "__main__":
    main()