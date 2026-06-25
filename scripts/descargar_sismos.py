"""
=============================================================
TALLER: Power BI Práctico — Datos sísmicos globales (USGS)
=============================================================
Autor del taller: (tu nombre)
Fuente de datos: USGS Earthquake Hazards Program
API pública: https://earthquake.usgs.gov/fdsnws/event/1/

Este script descarga datos de sismos globales usando la API
pública del USGS (United States Geological Survey) y genera
dos archivos CSV que usarás en Power BI:

  1. sismos.csv         → Tabla principal de eventos sísmicos
  2. zonas_riesgo.csv   → Tabla de clasificación de zonas por riesgo

No necesitas API key. La API del USGS es completamente pública.
=============================================================
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# ─────────────────────────────────────────────
# CONFIGURACIÓN  (puedes cambiar estos valores)
# ─────────────────────────────────────────────
DIAS_ATRAS      = 90        # Cuántos días hacia atrás consultar
MAGNITUD_MINIMA = 4.0       # Magnitud mínima (4.0+ son sismos perceptibles)
LIMITE          = 2000      # Máximo de registros a descargar
CARPETA_SALIDA  = "data"    # Carpeta donde se guardan los CSV

# ─────────────────────────────────────────────
# CONSTRUCCIÓN DE LA PETICIÓN A LA API
# ─────────────────────────────────────────────
fecha_fin    = datetime.utcnow()
fecha_inicio = fecha_fin - timedelta(days=DIAS_ATRAS)

parametros = {
    "format":     "geojson",
    "starttime":  fecha_inicio.strftime("%Y-%m-%d"),
    "endtime":    fecha_fin.strftime("%Y-%m-%d"),
    "minmagnitude": MAGNITUD_MINIMA,
    "limit":      LIMITE,
    "orderby":    "time"
}

URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# ─────────────────────────────────────────────
# DESCARGA
# ─────────────────────────────────────────────
print("=" * 60)
print("  Descargando sismos desde la API del USGS...")
print(f"  Período   : últimos {DIAS_ATRAS} días")
print(f"  Magnitud  : >= {MAGNITUD_MINIMA}")
print(f"  Límite    : {LIMITE} eventos")
print("=" * 60)

try:
    respuesta = requests.get(URL_BASE, params=parametros, timeout=30)
    respuesta.raise_for_status()
except requests.exceptions.Timeout:
    print("\n❌ ERROR: La petición tardó demasiado. Verifica tu conexión.")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No hay conexión a internet.")
    sys.exit(1)
except requests.exceptions.HTTPError as e:
    print(f"\n❌ ERROR HTTP: {e}")
    sys.exit(1)

datos_json = respuesta.json()
features   = datos_json.get("features", [])

if not features:
    print("\n⚠️  No se encontraron sismos con los parámetros dados.")
    sys.exit(0)

print(f"\n✅ Se descargaron {len(features)} eventos sísmicos.\n")

# ─────────────────────────────────────────────
# PROCESAMIENTO — Tabla 1: sismos.csv
# ─────────────────────────────────────────────
registros = []

for evento in features:
    props = evento.get("properties", {})
    geo   = evento.get("geometry", {}).get("coordinates", [None, None, None])

    # Convertir timestamp Unix (ms) a fecha legible
    ts_ms = props.get("time")
    if ts_ms:
        fecha_utc = datetime.utcfromtimestamp(ts_ms / 1000)
    else:
        fecha_utc = None

    magnitud   = props.get("mag")
    lugar      = props.get("place", "Sin descripción")
    tipo       = props.get("type", "earthquake")
    estado     = props.get("status", "desconocido")   # revisado / automático
    red        = props.get("net", "")                  # red sismológica que reportó
    alerta     = props.get("alert")                    # green / yellow / orange / red / None
    tsunami    = props.get("tsunami", 0)               # 1 si generó alerta de tsunami
    felt       = props.get("felt")                     # personas que reportaron sentirlo
    cdi        = props.get("cdi")                      # intensidad máxima reportada (Community)
    mmi        = props.get("mmi")                      # intensidad máxima instrumentada (ShakeMap)
    sig        = props.get("sig", 0)                   # significancia (0-1000)

    longitud   = geo[0]
    latitud    = geo[1]
    profundidad_km = geo[2]

    # Clasificación de profundidad
    if profundidad_km is None:
        tipo_profundidad = "Desconocida"
    elif profundidad_km < 70:
        tipo_profundidad = "Superficial"
    elif profundidad_km < 300:
        tipo_profundidad = "Intermedio"
    else:
        tipo_profundidad = "Profundo"

    # Clasificación de magnitud (escala Richter convencional)
    if magnitud is None:
        cat_magnitud = "Sin datos"
    elif magnitud < 4.5:
        cat_magnitud = "Leve (4.0-4.4)"
    elif magnitud < 5.0:
        cat_magnitud = "Moderado (4.5-4.9)"
    elif magnitud < 6.0:
        cat_magnitud = "Fuerte (5.0-5.9)"
    elif magnitud < 7.0:
        cat_magnitud = "Mayor (6.0-6.9)"
    else:
        cat_magnitud = "Gran sismo (7.0+)"

    # Extraer región aproximada del campo "place"
    # El lugar suele venir como "X km SSW of Ciudad, País"
    if lugar and "of" in lugar:
        partes = lugar.split("of", 1)
        region = partes[1].strip() if len(partes) > 1 else lugar
    else:
        region = lugar

    registros.append({
        "id_evento"       : evento.get("id", ""),
        "fecha_utc"       : fecha_utc.strftime("%Y-%m-%d %H:%M:%S") if fecha_utc else "",
        "fecha"           : fecha_utc.strftime("%Y-%m-%d") if fecha_utc else "",
        "hora"            : fecha_utc.strftime("%H:%M:%S") if fecha_utc else "",
        "anio"            : fecha_utc.year if fecha_utc else None,
        "mes"             : fecha_utc.month if fecha_utc else None,
        "dia_semana"      : fecha_utc.strftime("%A") if fecha_utc else "",
        "hora_del_dia"    : fecha_utc.hour if fecha_utc else None,
        "magnitud"        : magnitud,
        "categoria_magnitud": cat_magnitud,
        "profundidad_km"  : profundidad_km,
        "tipo_profundidad": tipo_profundidad,
        "latitud"         : latitud,
        "longitud"        : longitud,
        "lugar"           : lugar,
        "region"          : region,
        "tipo_evento"     : tipo,
        "red_sismologica" : red,
        "estado_revision" : estado,
        "nivel_alerta"    : alerta if alerta else "sin alerta",
        "alerta_tsunami"  : "Sí" if tsunami == 1 else "No",
        "reportes_publicos": felt if felt else 0,
        "intensidad_cdi"  : cdi,
        "intensidad_mmi"  : mmi,
        "significancia"   : sig,
    })

df_sismos = pd.DataFrame(registros)

# ─────────────────────────────────────────────
# PROCESAMIENTO — Tabla 2: zonas_riesgo.csv
# ─────────────────────────────────────────────
# Agregar por red sismológica + tipo de profundidad
# para crear una tabla de dimensión que relacionaremos en Power BI

df_zonas = (
    df_sismos
    .groupby(["red_sismologica", "tipo_profundidad"])
    .agg(
        total_sismos      = ("id_evento",       "count"),
        magnitud_promedio = ("magnitud",         "mean"),
        magnitud_maxima   = ("magnitud",         "max"),
        prof_promedio_km  = ("profundidad_km",   "mean"),
        sismos_con_alerta = ("nivel_alerta",     lambda x: (x != "sin alerta").sum()),
        alertas_tsunami   = ("alerta_tsunami",   lambda x: (x == "Sí").sum()),
        significancia_avg = ("significancia",    "mean"),
    )
    .reset_index()
)

df_zonas["magnitud_promedio"] = df_zonas["magnitud_promedio"].round(2)
df_zonas["prof_promedio_km"]  = df_zonas["prof_promedio_km"].round(1)
df_zonas["significancia_avg"] = df_zonas["significancia_avg"].round(1)

# Clasificación de riesgo por zona (combinación de factores)
def clasificar_riesgo(row):
    score = 0
    if row["magnitud_maxima"] >= 7.0:
        score += 3
    elif row["magnitud_maxima"] >= 6.0:
        score += 2
    elif row["magnitud_maxima"] >= 5.0:
        score += 1

    if row["alertas_tsunami"] > 0:
        score += 2
    if row["sismos_con_alerta"] > 0:
        score += 1
    if row["total_sismos"] > 50:
        score += 1

    if score >= 5:
        return "Muy alto"
    elif score >= 3:
        return "Alto"
    elif score >= 2:
        return "Moderado"
    else:
        return "Bajo"

df_zonas["nivel_riesgo"] = df_zonas.apply(clasificar_riesgo, axis=1)

# Clave de relación (la misma que usaremos en Power BI)
df_zonas["clave_zona"] = df_zonas["red_sismologica"] + "_" + df_zonas["tipo_profundidad"]
df_sismos["clave_zona"] = df_sismos["red_sismologica"] + "_" + df_sismos["tipo_profundidad"]

# ─────────────────────────────────────────────
# GUARDAR ARCHIVOS CSV
# ─────────────────────────────────────────────
os.makedirs(CARPETA_SALIDA, exist_ok=True)

ruta_sismos = os.path.join(CARPETA_SALIDA, "sismos.csv")
ruta_zonas  = os.path.join(CARPETA_SALIDA, "zonas_riesgo.csv")

df_sismos.to_csv(ruta_sismos, index=False, encoding="utf-8-sig")
df_zonas.to_csv(ruta_zonas,  index=False, encoding="utf-8-sig")

# ─────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────
print("─" * 60)
print("📄 ARCHIVOS GENERADOS")
print(f"   {ruta_sismos:<40} ({len(df_sismos):,} filas, {len(df_sismos.columns)} columnas)")
print(f"   {ruta_zonas:<40} ({len(df_zonas):,} filas, {len(df_zonas.columns)} columnas)")
print()
print("📊 ESTADÍSTICAS RÁPIDAS")
print(f"   Total de sismos descargados : {len(df_sismos):,}")
print(f"   Magnitud mínima             : {df_sismos['magnitud'].min()}")
print(f"   Magnitud máxima             : {df_sismos['magnitud'].max()}")
print(f"   Magnitud promedio           : {df_sismos['magnitud'].mean():.2f}")
print(f"   Sismos con alerta           : {(df_sismos['nivel_alerta'] != 'sin alerta').sum()}")
print(f"   Alertas de tsunami          : {(df_sismos['alerta_tsunami'] == 'Sí').sum()}")
print(f"   Redes sismológicas          : {df_sismos['red_sismologica'].nunique()}")
print(f"   Zonas identificadas         : {len(df_zonas)}")
print()
print("✅ ¡Listo! Abre Power BI Desktop e importa ambos CSV desde la carpeta 'data'.")
print("─" * 60)
