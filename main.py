from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from procesamiento import (
    generar_grafico_reservas,
    generar_grafico_minorista,
    generar_grafico_mayorista,
    generar_grafico_tasa_politica
)
import io

app = FastAPI(title="API BCRA - Visualización de Indicadores")

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API del BCRA - Gráficos"}

@app.get("/reservas")
def mostrar_reservas(
    anio_inicio: int = Query(2020), mes_inicio: int = Query(1),
    anio_final: int = Query(2024), mes_final: int = Query(12)
):
    imagen = generar_grafico_reservas(anio_inicio, mes_inicio, anio_final, mes_final)
    return StreamingResponse(io.BytesIO(imagen.getvalue()), media_type="image/png")

@app.get("/minorista")
def mostrar_minorista(
    anio_inicio: int = Query(2020), mes_inicio: int = Query(1),
    anio_final: int = Query(2024), mes_final: int = Query(12)
):
    imagen = generar_grafico_minorista(anio_inicio, mes_inicio, anio_final, mes_final)
    return StreamingResponse(io.BytesIO(imagen.getvalue()), media_type="image/png")

@app.get("/mayorista")
def mostrar_mayorista(
    anio_inicio: int = Query(2020), mes_inicio: int = Query(1),
    anio_final: int = Query(2024), mes_final: int = Query(12)
):
    imagen = generar_grafico_mayorista(anio_inicio, mes_inicio, anio_final, mes_final)
    return StreamingResponse(io.BytesIO(imagen.getvalue()), media_type="image/png")

@app.get("/tasa-politica")
def mostrar_tasa_politica(
    anio_inicio: int = Query(2020), mes_inicio: int = Query(1),
    anio_final: int = Query(2024), mes_final: int = Query(12)
):
    imagen = generar_grafico_tasa_politica(anio_inicio, mes_inicio, anio_final, mes_final)
    return StreamingResponse(io.BytesIO(imagen.getvalue()), media_type="image/png")
