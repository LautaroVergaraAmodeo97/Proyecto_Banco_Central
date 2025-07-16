import pandas as pd
import requests
import os

def cargar_historico(nombre_archivo):
    df = pd.read_csv(nombre_archivo, parse_dates=["Fecha"])
    return df

def obtener_datos_api(id_variable, desde):
    url = f"https://api.bcra.gob.ar/estadisticas/v3.0/Monetarias/{id_variable}"
    hasta = pd.Timestamp.today().strftime("%Y-%m-%d")
    params = {"desde": desde, "hasta": hasta}
    res = requests.get(url, params=params, verify=False)
    if res.status_code != 200:
        print(f"Error consultando API para variable {id_variable}")
        return pd.DataFrame()
    data = res.json().get("results", [])
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df["Fecha"] = pd.to_datetime(df["fecha"])
    df["Valor"] = df["valor"]
    return df[["Fecha", "Valor"]]

def actualizar_dataset(nombre_archivo_historico, id_variable, nombre_salida):
    df_hist = cargar_historico(nombre_archivo_historico)
    fecha_ultima = df_hist["Fecha"].max().strftime("%Y-%m-%d")
    df_api = obtener_datos_api(id_variable, fecha_ultima)
    df_final = pd.concat([df_hist, df_api], ignore_index=True)
    df_final = df_final.drop_duplicates(subset="Fecha").sort_values("Fecha")
    df_final.to_csv(os.path.join("data", nombre_salida), index=False)
    print(f"✅ Archivo actualizado: {nombre_salida}")

if __name__ == "__main__":
    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)

    actualizar_dataset(
        "Reserva en dolares desde 1996 hasta 2021.csv",
        1,
        "reservas_completas.csv"
    )

    actualizar_dataset(
        "Tipo de Cambio Minorista desde 2010 hasta 2021 - Hoja 1.csv",
        2,
        "tipo_cambio_minorista.csv"
    )

    actualizar_dataset(
        "Tipo de Cambio Mayorista desde 2002 hasta 2021 - Hoja 1.csv",
        3,
        "tipo_cambio_mayorista.csv"
    )

    actualizar_dataset(
        "Tasa de política monetaria en n.a desde 2015 hasta 2021 - Hoja 1.csv",
        4,
        "tasa_politica.csv"
    )
