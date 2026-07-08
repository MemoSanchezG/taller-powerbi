# 📅 Agenda — FUNDAMENTOS DE POWER BI: DEL DATASET AL DASHBOARD

**Duración total:** 5 horas  
**Dinámica:** 60% práctica / 40% teoría

---

## ⏱️ Distribución de tiempo

| # | Bloque | Tiempo | Acumulado |
|---|--------|--------|-----------|
| 1 | Introducción y contexto | 20 min | 00:20 |
| 2 | Python + API USGS | 30 min | 00:50 |
| — | Revisión de datos | 10 min | 01:00 |
| 3 | Power Query: carga y limpieza | 35 min | 01:35 |
| 4 | Power Query: columnas calculadas y query derivada | 30 min | 02:05 |
| 5 | Modelo de datos: relación entre tablas | 20 min | 02:25 |
| — | Revisión de modelo | 10 min | 02:35 |
| — | Receso | 15 min | 02:50 |
| 6 | Medidas DAX esenciales | 25 min | 03:15 |
| 7 | Visualización básica | 25 min | 03:40 |
| 8 | Dashboard avanzado + interactividad | 40 min | 04:20 |
| 9 | Reto guiado: construye tu propio visual | 20 min | 04:40 |
| 10 | Debate, preguntas y cierre | 20 min | 05:00 |

---

## 📋 Detalle de cada bloque

---

### Bloque 1 — Introducción y contexto (20 min)

**Objetivo:** Ubicar el taller en el flujo profesional de datos.

- ¿Qué es Business Intelligence y para qué sirve?
- El ecosistema de Power BI: Desktop, Service y Mobile (mención breve; hoy trabajamos en Desktop)
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
   git clone https://github.com/MemoSanchezG/taller-powerbi.git
   cd taller-powerbi
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

### Bloque 4 — Power Query: columnas calculadas y query derivada (30 min)

**Objetivo:** Crear columnas nuevas en Power Query y una query derivada.

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

#### Parte B — Columna adicional guiada: Turno del día (6 min)

1. En la query `sismos`, ir a **Add Column → Custom Column**
2. Nombre: `turno_dia`
3. Fórmula M:
   ```
   = if [hora_del_dia] < 6 then "Madrugada"
     else if [hora_del_dia] < 12 then "Mañana"
     else if [hora_del_dia] < 18 then "Tarde"
     else "Noche"
   ```
4. Cambiar tipo a **Text**
5. Este patrón `if / else if / else` es muy común para clasificar datos numéricos; se reutilizará en el reto del Bloque 9

#### Parte C — Query derivada: Solo sismos significativos (12 min)

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

### Bloque 5 — Modelo de datos: relación entre tablas (20 min)

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
> Este patrón (una tabla de hechos rodeada de dimensiones) se conoce como **esquema estrella**.

**¿Por qué "Single" y no "Both" en la dirección del filtro?**  
Con dirección única evitamos ambigüedades de filtrado cuando el modelo crece con más tablas de dimensión; "Both" solo se usa cuando realmente se necesita filtrar en ambos sentidos.

---

### Revisión de modelo (10 min)

---

### Receso (15 min)

Buen momento para estirarse, tomar café y resolver dudas 1:1. Si algún equipo se atrasó con los datos o la instalación, aprovechar para ponerse al corriente antes de continuar.

---

### Bloque 6 — Medidas DAX esenciales (25 min)

**Objetivo:** Introducir DAX y la diferencia entre medida y columna calculada.

#### Parte A — Concepto (5 min)
- Columna calculada (Power Query/M): se calcula fila por fila y queda fija al cargar el modelo
- Medida (DAX): se recalcula dinámicamente según el contexto de filtro activo (slicers, páginas, etc.)
- Sintaxis básica: `NombreMedida = Función(tabla[columna])`

#### Parte B — Práctica (15 min)

1. En el panel **Data**, clic derecho sobre la tabla `sismos` → **New measure**
2. Crear:
   ```
   Total Sismos = COUNTROWS(sismos)
   ```
3. Crear:
   ```
   Magnitud Promedio = AVERAGE(sismos[magnitud])
   ```
4. Crear:
   ```
   % Sismos Con Alerta =
   DIVIDE(
       CALCULATE(COUNTROWS(sismos), sismos[nivel_alerta] <> "sin alerta"),
       COUNTROWS(sismos)
   )
   ```
5. Formatear `% Sismos Con Alerta` como porcentaje (**Measure tool → Format → Percentage**)

#### Parte C — Discusión (5 min)
- ¿Por qué el valor de estas medidas cambia al aplicar un slicer, mientras que una columna calculada permanece igual?
- Estas medidas se usarán en el Bloque 7 en lugar de agregaciones directas

---

### Bloque 7 — Visualización básica (25 min)

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
2. Arrastrar la medida `Total Sismos` (creada en el Bloque 6) al campo **Fields**
3. Título: "Total de sismos registrados"

#### Visual 3 — Segmentador: filtro por nivel de alerta (10 min)

1. Insertar **Slicer**
2. Campo: `nivel_alerta`
3. Probar la interactividad: al seleccionar "red" en el slicer, la gráfica y la Card se filtran solas
4. **Este momento suele generar reacción — aprovecharlo para enfatizar la interactividad**

---

### Bloque 8 — Dashboard avanzado e interactividad (40 min)

**Objetivo:** Combinar datos de ambas tablas en visuales más ricos y agregar exploración ad hoc.

#### Visual 4 — Mapa de sismos (10 min)

1. Insertar visual **Map** (o **Azure Map** si está disponible)
2. Configurar:
   - **Location:** `latitud` + `longitud` (como coordenadas separadas)
   - **Size:** `magnitud` (burbujas más grandes = sismos más fuertes)
   - **Color:** `nivel_alerta`
3. Filtrar desde el mapa: hacer clic en una zona y ver cómo reacciona la gráfica de barras

#### Visual 5 — Tabla combinada: sismos + nivel de riesgo de zona (10 min)

Este visual usa datos de **ambas tablas** gracias a la relación que creamos.

1. Insertar visual **Table**
2. Columnas a incluir:
   - De `sismos`: `region`, `magnitud`, `categoria_magnitud`, `alerta_tsunami`
   - De `zonas_riesgo`: `nivel_riesgo`, `magnitud_maxima` (de la zona)
3. Ordenar por `magnitud` descendente
4. Resaltar: **estamos cruzando información de dos fuentes distintas en una sola vista**

#### Visual 6 — Gráfica de líneas: sismos por mes (10 min)

1. Insertar **Line Chart**
2. Configurar:
   - **X-axis:** `mes`
   - **Y-axis:** Count de `id_evento`
   - **Legend:** `tipo_profundidad`
3. Pregunta para el grupo: *¿Observan algún patrón temporal?*

#### Visual 7 — Drill-through: página de detalle por región (10 min)

1. Crear una nueva página llamada "Detalle región"
2. Agregar visuales de detalle: tabla con todos los sismos de la región, tarjetas con `Magnitud Promedio` y `% Sismos Con Alerta`
3. Arrastrar el campo `region` al pozo **Drillthrough** en el panel Visualizations
4. Volver a la página del dashboard principal → clic derecho sobre una barra o un punto del mapa → **Drill through → Detalle región**
5. Explicar el valor de esto para exploración ad hoc sin saturar el dashboard principal

---

### Bloque 9 — Reto guiado: construye tu propio visual (20 min)

**Objetivo:** Practicar de forma autónoma lo aprendido, con el instructor circulando por la sala resolviendo dudas.

Cada estudiante (o equipo) elige al menos **una** de estas opciones:

1. Crear una medida DAX nueva, por ejemplo `Sismo Mas Fuerte = MAX(sismos[magnitud])`
2. Agregar un visual no cubierto en la guía (Donut chart de `tipo_profundidad`, Treemap de `region`, o similar)
3. Aplicar formato condicional a la tabla combinada del Bloque 8 (colorear por `nivel_riesgo`)
4. Agregar un segundo slicer (por `categoria_magnitud` o un rango de fechas)
5. Replicar el patrón de `turno_dia` del Bloque 4, pero clasificando `dia_semana` en "Fin de semana" / "Día laboral"

Si el tiempo lo permite, invitar a 2–3 estudiantes a compartir su pantalla brevemente.

---

### Bloque 10 — Debate, preguntas y cierre (20 min)

**Preguntas guía para el debate:**

1. ¿En qué región del mundo se concentran más sismos? ¿Alguna hipótesis?
2. ¿Los sismos superficiales son más peligrosos que los profundos?
3. ¿Qué decisiones de política pública o ingeniería civil podrías tomar con este dashboard?
4. ¿Qué proyecto presentarías o qué rol tomarías en proyectos de ingeniería civil o política pública?
5. ¿Qué columna agregarías tú al dataset para hacer el análisis más completo?
6. ¿Qué ventaja le viste a una medida DAX frente a una columna calculada de Power Query?

**Cierre:**
- Compartir brevemente los retos resueltos en el Bloque 9 (si no se hizo antes)
- Recomendaciones para seguir aprendiendo: Microsoft Learn, Comunidad Power BI

---

## 🔧 Variaciones opcionales (si sobra tiempo)

- **Bookmarks y navegación:** crear botones para alternar entre el dashboard principal y la página de detalle
- **Tooltips personalizados:** página de tooltip con información adicional al pasar el mouse sobre el mapa
- **Filtro de fecha:** agregar un slicer de rango de fechas
- **Exportar el informe a PDF** desde Power BI

---

## ⚠️ Notas

- Si la API del USGS no responde, usar los datos del repositorio en `data/sismos_muestra.csv`
- Power BI puede tardar al cargar +1,000 filas en equipos lentos; ajustar `LIMITE = 500` en el script
- El visual de mapa requiere tener habilitado "Map and filled map visuals" en la configuración de Power BI (Security settings)
- El receso a la mitad del taller es buen momento para resolver problemas de instalación o de datos que hayan quedado pendientes
