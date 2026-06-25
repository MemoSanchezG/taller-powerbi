# 📅 Agenda — FUNDAMENTOS DE POWER BI: DEL DATASET AL DASHBOARD

**Duración total:** 3 horas 30 minutos  
**Dinámica:** 60% práctica / 40% teoría

---

## ⏱️ Distribución de tiempo

| # | Bloque | Tiempo | Acumulado |
|---|--------|--------|-----------|
| 1 | Introducción y contexto | 15 min | 00:15 |
| 2 | Python + API USGS | 30 min | 00:45 |
| — | Revisión de datos | 10 min | 00:55 |
| 3 | Power Query: carga y limpieza | 35 min | 01:30 |
| 4 | Power Query: columna calculada y 2 queries | 25 min | 01:55 |
| 5 | Modelo de datos: relación entre tablas | 15 min | 02:10 |
| — | Revisión de modelo | 10 min | 02:20 |
| 6 | Visualización básica | 25 min | 02:45 |
| 7 | Dashboard con visual avanzado + interactividad | 30 min | 03:15 |
| 8 | Exploración, preguntas y cierre | 15 min | 03:30 |

---

## 📋 Detalle de cada bloque

---

### Bloque 1 — Introducción y contexto (15 min)

**Objetivo:** Ubicar el taller en el flujo profesional de datos.

- ¿Qué es Business Intelligence y para qué sirve?
- Roles en el mundo de datos: analista, ingeniero, científico
- El ciclo completo: captura → limpieza → modelo → visualización
- ¿Por qué sismos? ¿Qué preguntas podemos responder con datos reales?
- Demostración rápida del resultado final (mostrar el dashboard terminado)
- Presentar el repositorio en GitHub

**Pregunta para el grupo:**  
> *"¿Cuántos sismos creen que ocurren en el mundo en un día cualquiera?"*

---

### Bloque 2 — Python + API USGS (30 min)

**Objetivo:** Consultar datos reales de una API y generar los CSV que usaremos en Power BI.

#### Parte A — Concepto (5 min)
- ¿Qué es una API REST? Analogía: menú de restaurante
- ¿Por qué usar datos de API en lugar de un Excel estático?
- El USGS registra todos los sismos globales en tiempo real
- No se necesita API key: es una fuente pública del gobierno de EE.UU.

#### Parte B — Práctica (20 min)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/taller-powerbi-sismos.git
   cd taller-powerbi-sismos
   ```

2. Instalar dependencias:
   ```bash
   pip install requests pandas
   ```

3. Explorar el script `descargar_sismos.py`:
   - Mostrar los parámetros configurables (días, magnitud mínima)
   - Explicar la estructura de la respuesta JSON del USGS
   - Señalar la lógica de clasificación de magnitud y profundidad

4. Ejecutar el script:
   ```bash
   python scripts/descargar_sismos.py
   ```

5. Revisar los CSV generados en la carpeta `data/`

#### Parte C — Discusión (5 min)
- ¿Cuántos eventos descargamos?
- ¿Cuál fue el sismo más grande del período?
- ¿Hay algún evento de México?

**Variables clave a destacar:**  
`magnitud`, `profundidad_km`, `tipo_profundidad`, `nivel_alerta`, `alerta_tsunami`, `clave_zona`

---

### Revisión de datos (10 min)

Este espacio se usa para asegurar que todos tengan datos para la entrada de Power BI.

---

### Bloque 3 — Power Query: carga y limpieza (35 min)

**Objetivo:** Importar los dos CSV a Power BI y aplicar transformaciones esenciales.

#### Paso 1 — Importar datos (10 min)

1. Abrir Power BI Desktop
2. **Home → Get data → Text/CSV**
3. Seleccionar `sismos.csv` → **Transform Data** (no Load)
4. Repetir para `zonas_riesgo.csv`
5. Notar que se abren dos **queries** en Power Query Editor

#### Paso 2 — Revisar tipos de datos (8 min)

En la query `sismos`:
- `magnitud` → Decimal Number
- `profundidad_km` → Decimal Number
- `latitud` / `longitud` → Decimal Number
- `mes`, `hora_del_dia`, `significancia` → Whole Number
- `fecha` → Date
- `alerta_tsunami`, `nivel_alerta`, `region` → Text

> ⚠️ Power Query detecta tipos automáticamente, pero siempre verificar.

#### Paso 3 — Limpieza básica (10 min)

- Filtrar filas donde `magnitud` sea nula (si las hay)
- En la query `sismos`: verificar que `clave_zona` está presente
- En la query `zonas_riesgo`: verificar que `clave_zona` también existe
- Renombrar las queries a nombres descriptivos si Power BI no lo hace

#### Paso 4 — Validar el número de filas (7 min)

- Mostrar la barra inferior de Power Query: "X rows loaded"
- Comparar con el resumen que imprimió el script Python
- Hablar de por qué es importante validar la integridad de los datos

---

### Bloque 4 — Power Query: columna calculada y filtro avanzado (25 min)

**Objetivo:** Crear una columna nueva en Power Query y hacer una query derivada.

#### Parte A — Nueva columna: Energía relativa (12 min)

La energía liberada por un sismo crece exponencialmente con la magnitud.  
Usaremos una aproximación práctica para visualizar esto.

1. En la query `sismos`, ir a **Add Column → Custom Column**
2. Nombre: `energia_relativa`
3. Fórmula M:
   ```
   = Number.Power(10, 1.5 * [magnitud])
   ```
4. Cambiar tipo de la nueva columna a **Decimal Number**
5. Discutir: *¿Cuántas veces más energía libera un sismo de magnitud 7 que uno de magnitud 5?*


#### Parte B — Query derivada: Solo sismos significativos (13 min)

Crearemos una segunda vista filtrada (query adicional) que Power BI puede usar en paralelo.

1. En el panel izquierdo de Power Query, clic derecho sobre `sismos`
2. **Duplicate** (o **Reference** — explicar la diferencia)
3. Renombrar como `sismos_significativos`
4. Filtrar: `significancia` >= 500
5. Filtrar: `nivel_alerta` ≠ "sin alerta"
6. Esta query mostrará solo los eventos que el USGS considera relevantes

> 📌 **Diferencia Reference vs Duplicate:**  
> - **Duplicate:** copia independiente (cualquier cambio en el original no se propaga)  
> - **Reference:** referencia viva (hereda todos los pasos del original)

7. Hacer clic en **Close & Apply**

---

### Bloque 5 — Modelo de datos: relación entre tablas (15 min)

**Objetivo:** Crear la relación entre `sismos` y `zonas_riesgo` usando `clave_zona`.

1. Ir a la vista **Model** (icono de diagrama en el panel izquierdo)
2. Observar las tres tablas: `sismos`, `sismos_significativos`, `zonas_riesgo`
3. Crear relación:
   - Arrastrar `clave_zona` de `sismos` hacia `clave_zona` de `zonas_riesgo`
   - Tipo: **Many to One (muchos a uno)**
   - Dirección del filtro: **Single**
4. Verificar la relación en el diagrama (línea que las une)

**Concepto clave — Tabla de hechos vs. tabla de dimensión:**  
> `sismos` = tabla de hechos (cada fila = un evento real)  
> `zonas_riesgo` = tabla de dimensión (describe/clasifica las zonas)

---

### Revisión (10 min)

---

### Bloque 6 — Visualización básica (25 min)

**Objetivo:** Crear el primer visual sencillo: distribución de sismos por categoría de magnitud.

#### Visual 1 — Gráfica de barras: conteo por categoría de magnitud (10 min)

1. Ir a la vista **Report**
2. En el panel Visualizations, seleccionar **Clustered Bar Chart**
3. Configurar:
   - **Y-axis:** `categoria_magnitud` (de la tabla `sismos`)
   - **X-axis:** `id_evento` → cambiar a **Count**
4. Dar formato: título "Sismos por categoría de magnitud"

#### Visual 2 — Tarjeta KPI: total de sismos (5 min)

1. Insertar visual **Card**
2. Campo: `id_evento` → Count
3. Título: "Total de sismos registrados"

#### Visual 3 — Segmentador: filtro por nivel de alerta (10 min)

1. Insertar **Slicer**
2. Campo: `nivel_alerta`
3. Probar la interactividad: al seleccionar "red" en el slicer, la gráfica se filtra sola
4. **Este momento suele generar reacción — aprovecharlo para enfatizar la interactividad**

---

### Bloque 7 — Dashboard con visual avanzado e interactividad (30 min)

**Objetivo:** Combinar datos de ambas tablas en un visual más rico.

#### Visual 4 — Mapa de sismos (10 min)

1. Insertar visual **Map** (o **Azure Map** si está disponible)
2. Configurar:
   - **Location:** `latitud` + `longitud` (como coordenadas separadas)
   - **Size:** `magnitud` (burbujas más grandes = sismos más fuertes)
   - **Color:** `nivel_alerta`
3. Filtrar desde el mapa: hacer clic en una zona y ver cómo reacciona la gráfica de barras

#### Visual 5 — Tabla combinada: sismos + nivel de riesgo de zona (12 min)

Este visual usa datos de **ambas tablas** gracias a la relación que creamos.

1. Insertar visual **Table**
2. Columnas a incluir:
   - De `sismos`: `region`, `magnitud`, `categoria_magnitud`, `alerta_tsunami`
   - De `zonas_riesgo`: `nivel_riesgo`, `magnitud_maxima` (de la zona)
3. Ordenar por `magnitud` descendente
4. Resaltar: **estamos cruzando información de dos fuentes distintas en una sola vista**

#### Visual 6 — Gráfica de líneas: sismos por mes (8 min)

1. Insertar **Line Chart**
2. Configurar:
   - **X-axis:** `mes`
   - **Y-axis:** Count de `id_evento`
   - **Legend:** `tipo_profundidad`
3. Pregunta para el grupo: *¿Observan algún patrón temporal?*

---

### Bloque 8 — Debate, preguntas y cierre (15 min)

**Preguntas guía para el debate:**

1. ¿En qué región del mundo se concentran más sismos? ¿Alguna hipótesis?
2. ¿Los sismos superficiales son más peligrosos que los profundos?
3. ¿Qué decisiones de política pública o ingeniería civil podrías tomar con este dashboard?
4. ¿Qué proyecto presentarías o que rol tomarías en proyectos de ingeniería civil o política pública?
5. ¿Qué columna agregarías tú al dataset para hacer el análisis más completo?

**Cierre:**
- Recomendaciones para seguir aprendiendo: Microsoft Learn, Comunidad Power BI

---

## 🔧 Variaciones opcionales (si sobra tiempo)

- **Condicional con DAX:** crear una medida `[% sismos con alerta]`
- **Drill-through:** configurar una página de detalle por región
- **Filtro de fecha:** agregar un slicer de rango de fechas
- **Exportar el informe a PDF** desde Power BI

---

## ⚠️ Notas

- Si la API del USGS no responde, usar los datos del repositorio en `data/sismos_muestra.csv`
- Power BI puede tardar al cargar +1,000 filas en equipos lentos; ajustar `LIMITE = 500` en el script
- El visual de mapa requiere tener habilitado "Map and filled map visuals" en la configuración de Power BI (Security settings)
