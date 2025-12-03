import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import os

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

def export_csv(df, path="reporte_interacciones.csv"):
    df.to_csv(path, index=False)
    return path

def export_pdf(summary_text, plot_paths=None, out="reporte_estadisticas.pdf"):
    doc = SimpleDocTemplate(out)
    styles = getSampleStyleSheet()
    elems = []
    elems.append(Paragraph("Reporte de Interacciones", styles["Title"]))
    elems.append(Spacer(1,12))
    elems.append(Paragraph(summary_text.replace("\n","<br/>"), styles["Normal"]))
    if plot_paths:
        for p in plot_paths:
            if os.path.exists(p):
                elems.append(Spacer(1,12))
                elems.append(Image(p, width=400, height=200))
    doc.build(elems)
    return out


if __name__ == "__main__":
    df, temas, horas = analisis_completo()

    print("\nGenerando gráficos...")
    grafico_temas(temas)
    grafico_horas(horas)