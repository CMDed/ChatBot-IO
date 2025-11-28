import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def cargar_stats(ruta="stats.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["registros"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hora"] = df["timestamp"].dt.hour
    return df


def analisis_temas(df):
    conteo = df["tema"].value_counts()
    print("\n=== TEMAS MÁS CONSULTADOS ===")
    print(conteo)
    return conteo


def analisis_horas(df):
    horas = df["hora"].value_counts().sort_index()
    print("\n=== FRECUENCIA POR HORA ===")
    print(horas)
    return horas


def analisis_completo():
    df = cargar_stats()
    print("\n>>> Estadísticas cargadas correctamente")

    temas = analisis_temas(df)
    horas = analisis_horas(df)

    return df, temas, horas

def grafico_temas(temas):
    plt.figure()
    temas.plot(kind="bar")
    plt.title("Temas más consultados")
    plt.xlabel("Tema")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

def grafico_horas(horas):
    plt.figure()
    horas.plot(kind="bar")
    plt.title("Actividad por hora del día")
    plt.xlabel("Hora")
    plt.ylabel("Consultas")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df, temas, horas = analisis_completo()

    print("\nGenerando gráficos...")
    grafico_temas(temas)
    grafico_horas(horas)