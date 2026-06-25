# 📖 Guía Power BI — FUNDAMENTOS DE POWER BI: DEL DATASET AL DASHBOARD

> Sigue esta guía después de ejecutar el script Python y tener los archivos  
> `sismos.csv` y `zonas_riesgo.csv` en la carpeta `data/`.

---

## Paso 1 — Abrir Power BI Desktop

1. Abre **Power BI Desktop**
2. En la pantalla de inicio, cierra el cuadro de diálogo inicial
3. Guarda el archivo como `taller_sismos.pbix` antes de empezar

---

## Paso 2 — Importar los datos

1. Ve a **Home → Get data → Text/CSV**
2. Navega a la carpeta `data/` y selecciona `sismos.csv`
3. Se abre una vista previa del archivo → haz clic en **Transform Data**  
   *(Esto abre Power Query Editor — NO hagas clic en "Load" todavía)*
4. Repite el proceso: **New Source → Text/CSV** → selecciona `zonas_riesgo.csv`
5. Ahora debes ver **dos queries** en el panel izquierdo de Power Query

---

## Paso 3 — Revisar y corregir tipos de datos en `sismos`

En el panel izquierdo, selecciona la query **`sismos`**.

Verifica que cada columna tenga el tipo correcto (el ícono a la izquierda del nombre):

| Columna | Tipo correcto |
|---------|--------------|
| `magnitud` | Decimal Number |
| `profundidad_km` | Decimal Number |
| `latitud` / `longitud` | Decimal Number |
| `mes`, `hora_del_dia` | Whole Number |
| `significancia` | Whole Number |
| `fecha` | Date |
| `fecha_utc` | Text (o Date/Time) |
| `nivel_alerta`, `region`, `clave_zona` | Text |

Para cambiar el tipo: clic en el encabezado de la columna → **Change Type**

---

## Paso 4 — Crear columna calculada: Energía relativa

Esta columna nos permitirá comparar visualmente cuánta energía libera cada sismo,  
usando la relación entre magnitud y energía (escala logarítmica).

1. En la query `sismos`, ve a **Add Column → Custom Column**
2. Nombre de la columna: `energia_relativa`
3. Escribe esta fórmula:
   ```
   = Number.Power(10, 1.5 * [magnitud])
   ```
4. Haz clic en **OK**
5. La nueva columna aparecerá al final de la tabla
6. Cambia su tipo a **Decimal Number**

> 💡 **¿Por qué 1.5 × magnitud?**  
> La relación entre magnitud de momento y energía es:  
> `log₁₀(E) ≈ 1.5 × M + constante`  
> Un sismo de M6 libera ~31 veces más energía que uno de M5,  
> y uno de M7 libera ~1,000 veces más que uno de M5.

---

## Paso 5 — Crear segunda query: Sismos significativos

Crearemos una vista filtrada que solo muestre los eventos más relevantes.

1. En el panel izquierdo, haz **clic derecho sobre la query `sismos`**
2. Selecciona **Reference**  
   *(Reference = la nueva query hereda todos los pasos de `sismos`)*
3. Renombra la nueva query como `sismos_significativos`  
   *(clic derecho sobre ella en el panel izquierdo → Rename)*
4. Aplica estos dos filtros:
   - Clic en la flecha de la columna `significancia` → **Number Filters → Greater than or equal to** → 500
   - Clic en la flecha de `nivel_alerta` → desmarcar "sin alerta" → **OK**
5. Esta query ahora muestra solo los sismos que el USGS considera altamente relevantes

> 📌 **Reference vs. Duplicate:**  
> - **Reference:** si modificas `sismos`, los cambios se propagan a `sismos_significativos`  
> - **Duplicate:** copia independiente; los cambios en el original no la afectan

---

## Paso 6 — Aplicar y cargar

1. Haz clic en **Close & Apply** (esquina superior izquierda). Esto cerrará Power Query, lo puedes abrir en cualquier momento usando el botón "Transform data"
2. Power BI cargará las tres queries: `sismos`, `sismos_significativos`, `zonas_riesgo`
3. Una vez cargadas, verás las tablas en el panel **Data** (derecha)

---

## Paso 7 — Crear la relación entre tablas

1. Haz clic en el ícono de **Model** en el panel izquierdo (parece un diagrama de red)
2. Verás las tres tablas como tarjetas
3. **Arrastra** el campo `clave_zona` de la tabla `sismos` hasta el campo `clave_zona` de `zonas_riesgo`
4. Se abrirá el diálogo "Create relationship":
   - **Cardinality:** Many to One (Many:1)
   - **Cross filter direction:** Single
   - Haz clic en **OK**
5. Aparecerá una línea conectando ambas tablas ✅

---

## Paso 8 — Visual 1: Gráfica de barras por categoría de magnitud

1. Ve a la vista **Report** (ícono de gráfica en el panel izquierdo)
2. En el panel **Visualizations**, selecciona **Clustered Bar Chart**
3. Arrastra desde el panel **Data**:
   - `categoria_magnitud` → campo **Y-axis**
   - `id_evento` → campo **X-axis** (luego cambia la agregación a **Count**)
4. Formato sugerido:
   - Título: "Sismos por categoría de magnitud"
   - Colores: usa una paleta de riesgo (verde → amarillo → rojo)

---

## Paso 9 — Visual 2: Tarjeta KPI — Total de sismos

1. Haz clic en un área vacía del lienzo
2. Selecciona el visual **Card**
3. Arrastra `id_evento` al campo **Fields** → cambia la agregación a **Count**
4. Título: "Total de sismos registrados"

---

## Paso 10 — Visual 3: Segmentador por nivel de alerta

1. Haz clic en un área vacía del lienzo
2. Selecciona el visual **Slicer**
3. Arrastra `nivel_alerta` al campo **Field**
4. Prueba seleccionar diferentes alertas y observa cómo se actualiza la gráfica de barras

---

## Paso 11 — Visual 4: Mapa de epicentros

> ⚠️ Antes de insertar el mapa: ve a **File → Options → Security**  
> y habilita **"Map and filled map visuals"** si no está activado.

1. Haz clic en un área vacía del lienzo
2. Selecciona el visual **Map**
3. Configura:
   - **Latitude:** `latitud`
   - **Longitude:** `longitud`
   - **Size:** `magnitud` (burbujas más grandes = sismos más fuertes)
   - **Color saturation:** `significancia`
4. Haz clic en una burbuja del mapa → observa cómo los otros visuales se filtran automáticamente

---

## Paso 12 — Visual 5: Tabla combinada (datos de 2 tablas)

Este es el visual que demuestra el valor de haber creado la relación entre tablas.

1. Selecciona el visual **Table**
2. Agrega las siguientes columnas:
   - De `sismos`: `region`, `magnitud`, `categoria_magnitud`, `alerta_tsunami`, `tipo_profundidad`
   - De `zonas_riesgo`: `nivel_riesgo`, `magnitud_maxima`
3. Ordena por `magnitud` de forma descendente
4. Nota cómo la columna `nivel_riesgo` viene de una tabla diferente, pero Power BI la cruza automáticamente gracias a la relación

---

## Paso 13 — Visual 6: Líneas de tiempo — sismos por mes

1. Selecciona el visual **Line Chart**
2. Configura:
   - **X-axis:** `mes`
   - **Y-axis:** `id_evento` → Count
   - **Legend:** `tipo_profundidad`
3. Observa si hay variación temporal en la frecuencia de sismos por tipo de profundidad

---

## Resultado final esperado

Tu dashboard debería tener:

```
┌─────────────────────────────────────────────────────────┐
│  [Slicer: nivel_alerta]    [Card: Total sismos]         │
│                                                         │
│  [Bar Chart: por categoría]   [Map: epicentros]         │
│                                                         │
│  [Table: región + nivel_riesgo (2 tablas)]              │
│                                                         │
│  [Line Chart: por mes y tipo de profundidad]            │
└─────────────────────────────────────────────────────────┘
```

---

## Fórmulas M útiles para explorar por tu cuenta

```
// Clasificar hora del día
= if [hora_del_dia] < 6 then "Madrugada"
  else if [hora_del_dia] < 12 then "Mañana"
  else if [hora_del_dia] < 18 then "Tarde"
  else "Noche"

// Identificar si el sismo fue en fin de semana
= if [dia_semana] = "Saturday" or [dia_semana] = "Sunday"
  then "Fin de semana" else "Día laboral"

// Energía en joules (aproximación)
= Number.Power(10, 1.5 * [magnitud] + 4.8)
```

---

## Preguntas para reflexionar con tu dashboard

1. ¿Cuál es el sismo más grande registrado en el período?
2. ¿Qué red sismológica reportó más eventos?
3. ¿Los sismos superficiales tienden a ser más o menos fuertes que los profundos?
4. ¿En qué hora del día ocurren más sismos? *(spoiler: los sismos no tienen horario)*
5. ¿Qué porcentaje de los sismos generó algún nivel de alerta?
