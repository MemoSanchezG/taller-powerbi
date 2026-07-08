# FUNDAMENTOS DE POWER BI: DEL DATASET AL DASHBOARD

> **FCFM – UANL** | Duración: 5 horas  
> Nivel: Introductorio-Intermedio | Sin conocimientos previos de Power BI requeridos

---

## 🎯 ¿Qué aprenderás?

| Etapa | Contenido |
|-------|-----------|
| 1 | Qué es Business Intelligence y por qué nos importa |
| 2 | Consultar una API pública con Python y generar datos reales |
| 3 | Importar y limpiar datos en Power Query |
| 4 | Crear columnas calculadas y aplicar fórmulas en Power Query |
| 5 | Relacionar dos tablas en el modelo de datos |
| 6 | Construir visualizaciones interactivas en Power BI |
| 7 | Leer e interpretar un dashboard |

---

## 📦 Estructura del repositorio

```
taller-powerbi-sismos/
│
├── scripts/
│   └── descargar_sismos.py     ← Script Python que consulta la API
│
├── data/                        ← Los CSV se generan aquí (no incluidos en el repo)
│   ├── sismos.csv               ← Tabla principal: un evento sísmico por fila
│   └── zonas_riesgo.csv         ← Tabla de dimensión: clasificación por zona/profundidad
│
├── guia/
│   ├── agenda.md                ← Agenda detallada del taller (5h)
│   └── guia_powerbi.md          ← Paso a paso para Power Query, DAX y los visuales
│
├── presentacion/
│   └── taller_powerbi.tex       ← Diapositivas (LaTeX/Beamer) para el instructor
│
└── README.md                    ← Este archivo
```

---

## 🛠️ Requisitos

### Python
```
Python 3.8+
requests
pandas
```

Instala las dependencias con:
```bash
pip install requests pandas
```

### Power BI
- **Power BI Desktop** (gratuito): https://powerbi.microsoft.com/desktop
- Conexión a internet (solo para la descarga inicial de datos)

---

## 🚀 Pasos para ejecutar

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/taller-powerbi-sismos.git
cd taller-powerbi-sismos
```

### 2. Instalar dependencias
```bash
pip install requests pandas
```

### 3. Descargar los datos sísmicos
```bash
python scripts/descargar_sismos.py
```

Esto consultará la **API pública del USGS** y generará dos archivos en la carpeta `data/`:
- `sismos.csv` — Eventos sísmicos de los últimos 90 días (magnitud ≥ 4.0)
- `zonas_riesgo.csv` — Tabla de resumen por red sismológica y tipo de profundidad

> ⚡ **Sin API key necesaria.** La API del USGS es completamente pública y gratuita. En otros proyectos puedes necesitar una API key, pueden ser gratis, gratis con registro o de paga.

### 4. Abrir Power BI Desktop
- Importa `sismos.csv` y `zonas_riesgo.csv`
- Sigue la [guía de Power BI](guia/guia_powerbi.md)

---

## 📊 Datos: USGS Earthquake Hazards Program

- **Fuente**: [earthquake.usgs.gov](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Cobertura**: Global, tiempo real
- **Actualización**: Continua (datos de los últimos 90 días por defecto)
- **Licencia**: Dominio público (datos del gobierno de EE.UU.)

### Variables principales en `sismos.csv`

| Columna | Descripción |
|---------|-------------|
| `id_evento` | Identificador único del USGS |
| `fecha_utc` | Fecha y hora en UTC |
| `magnitud` | Magnitud del sismo |
| `categoria_magnitud` | Clasificación: Leve / Moderado / Fuerte / Mayor / Gran sismo |
| `profundidad_km` | Profundidad del hipocentro en km |
| `tipo_profundidad` | Superficial (<70km) / Intermedio / Profundo (>300km) |
| `latitud` / `longitud` | Coordenadas del epicentro |
| `region` | Nombre de la región |
| `nivel_alerta` | green / yellow / orange / red / sin alerta |
| `alerta_tsunami` | Sí / No |
| `significancia` | Índice de importancia del evento (0–1000) |
| `clave_zona` | Clave de relación con `zonas_riesgo.csv` |

---

## 💡 Preguntas

- ¿Qué zona concentra la mayoría de los sismos?
- ¿Existe relación entre la profundidad del sismo y su magnitud percibida?
- ¿Los sismos superficiales son más peligrosos que los profundos?
- ¿Cómo se distribuyen los eventos a lo largo de la semana? ¿Hay patrones temporales?
- ¿Qué tan frecuentes son los sismos de magnitud 7.0+?

---

## 📚 Recursos para seguir aprendiendo

| Recurso | Enlace |
|---------|--------|
| Microsoft Learn – Power BI | https://learn.microsoft.com/es-es/training/powerplatform/power-bi |
| Documentación API USGS | https://earthquake.usgs.gov/fdsnws/event/1/ |
| Comunidad Power BI | https://community.fabric.microsoft.com |
| DAX Guide | https://dax.guide |

---

## 📝 Licencia

El código de este repositorio está bajo licencia **MIT**.  
Los datos sísmicos provienen del USGS y son de dominio público.
