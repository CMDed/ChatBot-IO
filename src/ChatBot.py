from datetime import datetime
import os
from data_loader import load_info
from core import process_message
from io_actions import IOAction, interpret
from analytics import compute_stats_and_plot
import json

def registrar_estadistica(tema, ruta="stats.json"):
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({"registros": []}, f, indent=2)

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["registros"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tema": tema
    })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    print("Bienvenido a MentorCORE. Escribe 'salir' para terminar. Escribe 'comandos' para listar todos los comandos disponibles.\n")

    try:
        respuestas, reglas, sinonimos_inversos, respuestas_avanzadas = load_info('info.json')

        with open('info.json', 'r', encoding='utf-8') as f:
            data_info = json.load(f)
        respuestas_avanzadas = data_info.get('respuestas_avanzadas', {})

    except FileNotFoundError:
        print("Error: No se encontró 'info.json'. Deteniendo programa.")
        return
    
    except Exception as e:
        print(f"Error al cargar info.json: {e}")
        return

    from data_loader import create_inverse_synonyms

    modo = "basico"  #basico y avanzado

    while True:
        message = interpret(IOAction("Input"))
        if message is None:
            continue

        if message.lower() == "salir":
            print("Hasta luego.")
            break

        if message == "modo basico":
            modo = "basico"
            interpret(IOAction("Output", "Modo básico activado."))
            continue
        
        if message == "modo avanzado":
            modo = "avanzado"
            interpret(IOAction("Output", "Modo avanzado activado."))
            continue

        if message.strip().lower() == "comandos":
            interpret(IOAction("Output",
                "Comandos disponibles:\n"
                "- estadisticas: muestra análisis del uso del bot\n"
                "- estadisticas hora: muestra análisis del uso del bot por horas\n"
                "- agregar sinonimo X = Y: añade un nuevo sinónimo (Y es la base, X es el sinónimo)\n"
                "- modo basico / modo avanzado: cambia nivel de detalle\n"
                "- salir: termina el programa\n"
            ))
            continue

        if message.startswith("agregar sinonimo"):
            try:
                _, resto = message.split("agregar sinonimo", 1)
                resto = resto.strip()
                
                base, nuevo = map(lambda x: x.strip(), resto.split("=", 1))
                
                sinonimo_ingresado = base
                palabra_base = nuevo

                with open("info.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                if palabra_base in data["sinonimos"]:
                    if sinonimo_ingresado not in data["sinonimos"][palabra_base]:
                        data["sinonimos"][palabra_base].append(sinonimo_ingresado)
                    else:
                        interpret(IOAction("Output", f"El sinónimo '{sinonimo_ingresado}' ya existe para la base '{palabra_base}'."))
                        continue
                else:
                    data["sinonimos"][palabra_base] = [sinonimo_ingresado]

                with open("info.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                sinonimos_inversos = create_inverse_synonyms(data["sinonimos"])

                interpret(IOAction("Output", f"Sinónimo agregado con éxito: '{sinonimo_ingresado}' ahora se mapea a la base '{palabra_base}'."))
            except ValueError:
                interpret(IOAction("Output", "Error de formato. Usa: agregar sinonimo SINÓNIMO = BASE"))
            except Exception as e:
                interpret(IOAction("Output", f"Error inesperado al agregar sinónimo: {e}"))

            continue

        if message.strip().lower() in ["estadisticas", "estadísticas", "stats"]:
            res = compute_stats_and_plot()
            if res["plot"]:
                interpret(IOAction("Output", f"Resumen de intenciones:\n{res['message']}"))
                interpret(IOAction("Output", f"Gráfico guardado en: {res['plot']}"))
            else:
                interpret(IOAction("Output", res["message"]))
            continue

        if message == "estadisticas hora":
            from analytics import plot_by_hour
            path = plot_by_hour()
            if path:
                interpret(IOAction("Output", f"Gráfico creado: {path}"))
            else:
                interpret(IOAction("Output", "No hay datos suficientes"))
            continue

        # Procesamiento normal del mensaje
        coincidencia, response_text = process_message(message, reglas, respuestas, sinonimos_inversos)

        registrar_estadistica(coincidencia if coincidencia else "fallback")

        # registro de intecion
        interpret(IOAction("LogIntent", coincidencia))

        if modo == "avanzado":
    
            if coincidencia in respuestas_avanzadas:
                response_text = respuestas_avanzadas[coincidencia]
            else:
                response_text += "\n\n[Puedo darte una explicación más profunda si lo deseas]"
        
        # registro de respuesta
        interpret(IOAction("Output", response_text))

if __name__ == "__main__":
    main()