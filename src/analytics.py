import os
import csv
from datetime import datetime

ANALYTICS_FILE = "analytics.csv"

def ensure_file():
    if not os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "intent"])

def log_intent(intent_name):
    ensure_file()
    timestamp = datetime.utcnow().isoformat()
    intent_name = intent_name if intent_name is not None else "No encontrado"
    with open(ANALYTICS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, intent_name])

def compute_stats_and_plot(output_path="intents_plot.png"):
    import pandas as pd
    import matplotlib.pyplot as plt

    ensure_file()
    df = pd.read_csv(ANALYTICS_FILE, parse_dates=["timestamp"])
    if df.empty:
        return {"message": "No hay datos para mostrar aún.", "plot": None}

    conteo = df['intent'].value_counts()
    porcentaje = (conteo / conteo.sum()) * 100

    resumen_lines = []
    for intent, cnt in conteo.items():
        pct = porcentaje[intent]
        resumen_lines.append(f"- {intent}: {cnt} ({pct:.1f}%)")
    resumen = "\n".join(resumen_lines)

    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar")
    plt.title("Conteo de intenciones detectadas")
    plt.xlabel("Intención")
    plt.ylabel("Veces detectada")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"message": resumen, "plot": output_path}