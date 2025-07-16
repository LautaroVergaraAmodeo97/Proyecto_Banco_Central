import pandas as pd
import matplotlib.pyplot as plt
import io
import os

def cargar_csv(nombre_archivo):
    path = os.path.join("data", nombre_archivo)
    df = pd.read_csv(path, parse_dates=["fecha"])
    return df

def generar_grafico(df, anio_ini, mes_ini, anio_fin, mes_fin, titulo, ylabel):
    fecha_inicio = pd.to_datetime(f"{anio_ini}-{mes_ini:02d}-01")
    fecha_final = pd.to_datetime(f"{anio_fin}-{mes_fin:02d}-01")

    df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_final)].copy()
    df['anio'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    resumen = (
        df.groupby([df['fecha'].dt.to_period('M')])['valor']
        .mean()
        .reset_index()
    )
    resumen['fecha'] = resumen['fecha'].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(resumen['fecha'], resumen['valor'], marker='o')
    ax.set_title(titulo)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(ylabel)
    ax.grid(True)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def generar_grafico_reservas(anio_ini, mes_ini, anio_fin, mes_fin):
    df = cargar_csv("reservas_completas.csv")
    return generar_grafico(df, anio_ini, mes_ini, anio_fin, mes_fin,
                           "Reservas Internacionales del BCRA", "Millones de USD")

def generar_grafico_minorista(anio_ini, mes_ini, anio_fin, mes_fin):
    df = cargar_csv("tipo_cambio_minorista.csv")
    return generar_grafico(df, anio_ini, mes_ini, anio_fin, mes_fin,
                           "Tipo de Cambio Minorista", "ARS por USD")

def generar_grafico_mayorista(anio_ini, mes_ini, anio_fin, mes_fin):
    df = cargar_csv("tipo_cambio_mayorista.csv")
    return generar_grafico(df, anio_ini, mes_ini, anio_fin, mes_fin,
                           "Tipo de Cambio Mayorista", "ARS por USD")

def generar_grafico_tasa_politica(anio_ini, mes_ini, anio_fin, mes_fin):
    df = cargar_csv("tasa_politica.csv")
    return generar_grafico(df, anio_ini, mes_ini, anio_fin, mes_fin,
                           "Tasa de Política Monetaria", "%")
