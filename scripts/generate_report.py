"""Agente Redactor.

Genera el informe académico final en PDF (docs/informe_final.pdf) a partir de
las tablas producidas por los agentes de análisis económico y econométrico.
Reproducible: no requiere herramientas externas, solo fpdf2 (pip).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "outputs" / "tables"
OUTPUT_PATH = ROOT / "docs" / "informe_final.pdf"

MARGIN = 18


class ReportPDF(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Analisis del Contexto Nacional y Global - Inflacion en Ecuador (2014-2024)", align="L")
        self.ln(10)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def h1(pdf: ReportPDF, text: str) -> None:
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.ln(4)
    pdf.multi_cell(0, 9, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def h2(pdf: ReportPDF, text: str) -> None:
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(2)
    pdf.multi_cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def body(pdf: ReportPDF, text: str) -> None:
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5.6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def bullet(pdf: ReportPDF, text: str) -> None:
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5.6, f"-  {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def table(
    pdf: ReportPDF,
    df: pd.DataFrame,
    col_widths: list[float] | None = None,
    headers: list[str] | None = None,
) -> None:
    n_cols = len(df.columns)
    usable_width = pdf.w - 2 * MARGIN

    raw_widths = col_widths or [usable_width / n_cols] * n_cols
    if len(raw_widths) != n_cols:
        raw_widths = [usable_width / n_cols] * n_cols
    scale = usable_width / sum(raw_widths)
    widths = [w * scale for w in raw_widths]

    display_headers = headers or list(df.columns)

    pdf.set_x(MARGIN)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(230, 230, 230)
    for col, w in zip(display_headers, widths):
        pdf.cell(w, 7, str(col), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7.5)
    for _, row in df.iterrows():
        pdf.set_x(MARGIN)
        for val, w in zip(row, widths):
            text = f"{val:.2f}" if isinstance(val, float) else str(val)
            pdf.cell(w, 6, text, border=1)
        pdf.ln()
    pdf.ln(3)


def load_table(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES_DIR / name)


def build_pdf() -> None:
    pdf = ReportPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(MARGIN, 15, MARGIN)

    comparativos = load_table("indicadores_comparativos.csv")
    descriptivas = load_table("estadisticas_descriptivas.csv")
    correlaciones = load_table("correlaciones.csv")
    regresion = load_table("regresion_ecuador_eeuu.csv")
    volatilidad = load_table("volatilidad_inflacion.csv")
    pre_post = load_table("comparacion_pre_post_pandemia.csv")

    # Portada
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 15, 15)
    pdf.multi_cell(0, 12, "Analisis del Contexto Economico Nacional y Global", align="C")
    pdf.set_font("Helvetica", "", 15)
    pdf.ln(4)
    pdf.multi_cell(0, 8, "La inflacion en Ecuador (2014-2024) en el contexto de la dolarizacion:\ncomparacion con Estados Unidos, Peru, Panama y America Latina y el Caribe", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, "Economia - Octavo Semestre\nAsignatura: Analisis del Contexto Nacional y Global\nProyecto multiagentico de analisis economico", align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, "Quito, Ecuador - 2026", align="C")

    # Resumen ejecutivo
    pdf.add_page()
    h1(pdf, "Resumen Ejecutivo")
    body(
        pdf,
        "Este informe analiza la evolucion de la inflacion en Ecuador entre 2014 y 2024, contrastandola "
        "con Estados Unidos, Peru, Panama y el promedio de America Latina y el Caribe (excl. altos ingresos). "
        "Ecuador, como economia oficialmente dolarizada desde el ano 2000, carece de politica monetaria propia, "
        "por lo que su trayectoria inflacionaria depende en gran medida de la inflacion de su economia ancla "
        "(Estados Unidos) y de choques externos. Los resultados muestran que la inflacion ecuatoriana fue, en "
        "promedio, la mas baja y estable del grupo comparado en el periodo analizado, en linea con la hipotesis "
        "de disciplina de precios asociada a la dolarizacion, aunque esto tambien implica una perdida de "
        "herramientas de politica economica ante choques adversos."
    )

    # Introduccion
    h1(pdf, "1. Introduccion")
    body(
        pdf,
        "La estabilidad de precios es una de las variables macroeconomicas mas relevantes para evaluar el "
        "desempeno de una economia. En el caso ecuatoriano, esta estabilidad esta intrinsecamente ligada al "
        "regimen de dolarizacion vigente desde el ano 2000, que elimino la posibilidad de emision monetaria "
        "discrecional y ancla la economia domestica a la politica monetaria de Estados Unidos."
    )

    # Planteamiento del problema
    h1(pdf, "2. Planteamiento del Problema")
    body(
        pdf,
        "Pregunta de investigacion: ¿como se ha comportado la inflacion en Ecuador durante el periodo 2014-2024 "
        "en comparacion con economias de referencia, y en que medida esta trayectoria puede explicarse por su "
        "condicion de economia dolarizada?"
    )

    # Objetivos
    h1(pdf, "3. Objetivos")
    h2(pdf, "Objetivo general")
    body(pdf, "Analizar el comportamiento de la inflacion en Ecuador entre 2014 y 2024 en el contexto internacional.")
    h2(pdf, "Objetivos especificos")
    for obj in [
        "Recopilar y validar series de inflacion, PIB y desempleo de fuente oficial.",
        "Calcular indicadores descriptivos y de volatilidad de la inflacion.",
        "Analizar la correlacion entre inflacion, crecimiento economico y desempleo.",
        "Estimar la relacion entre la inflacion de Ecuador y la de Estados Unidos.",
        "Visualizar los resultados en un dashboard publico e interpretarlos economicamente.",
    ]:
        bullet(pdf, obj)

    # Marco conceptual
    pdf.add_page()
    h1(pdf, "4. Marco Conceptual")
    body(
        pdf,
        "Dolarizacion oficial: adopcion del dolar estadounidense como moneda de curso legal, renunciando a la "
        "politica monetaria y cambiaria propia a cambio de estabilidad de precios (Ecuador, 2000). Al no emitir "
        "moneda propia, el Banco Central del Ecuador pierde su rol tradicional de prestamista de ultima instancia "
        "y de emisor de politica monetaria contraciclica, por lo que el ajuste ante choques recae principalmente "
        "en la politica fiscal y en la flexibilidad de precios y salarios internos.\n\n"
        "Areas monetarias optimas (Mundell, 1961): marco teorico que evalua bajo que condiciones compartir "
        "moneda resulta beneficioso para una economia, considerando la movilidad de factores productivos, el "
        "grado de integracion comercial y la simetria de los choques que enfrentan los paises que comparten "
        "moneda. Ecuador y Estados Unidos no conforman, en sentido estricto, un area monetaria optima segun "
        "estos criterios, lo que hace mas relevante evaluar empiricamente el comportamiento de la inflacion "
        "ecuatoriana bajo este regimen.\n\n"
        "Inflacion importada: mecanismo por el cual la inflacion de la economia ancla se transmite a la economia "
        "dolarizada via precios de bienes transables (importaciones, insumos, combustibles) que se cotizan en "
        "dolares.\n\n"
        "Curva de Phillips: relacion (no necesariamente estable en el tiempo) entre inflacion y desempleo, usada "
        "aqui como marco de referencia para explorar los datos, no como ley universal. Este proyecto reporta la "
        "correlacion inflacion-desempleo por pais (seccion 10.4) como una exploracion empirica de esta relacion, "
        "sin asumir a priori que debe cumplirse."
    )

    # Contexto nacional
    h1(pdf, "5. Contexto Nacional (Ecuador)")
    body(
        pdf,
        "Ecuador ha mantenido, en el periodo analizado, niveles de inflacion consistentemente bajos, incluyendo "
        "anos de deflacion leve (-0.34% en 2020 y -0.22% en 2018, segun el Banco Mundial). Esto contrasta con "
        "episodios previos a la dolarizacion, en los que la inflacion ecuatoriana alcanzo niveles de dos y tres "
        "digitos anuales durante la crisis financiera de finales de la decada de 1990. La ausencia de politica "
        "monetaria propia limita la capacidad de respuesta ante choques como la caida del precio del petroleo "
        "(principal producto de exportacion del pais) o crisis externas, y traslada el peso del ajuste "
        "macroeconomico hacia la politica fiscal y hacia la competitividad real de la economia.\n\n"
        "El pico de inflacion del periodo (3.47% en 2022) se ubica muy por debajo de los picos observados en "
        "Peru (8.33%) o Estados Unidos (8.00%) el mismo ano, lo que sugiere una transmision parcial, y no total, "
        "de los choques inflacionarios externos hacia los precios domesticos ecuatorianos."
    )

    # Contexto global
    h1(pdf, "6. Contexto Global")
    body(
        pdf,
        "El periodo 2020-2024 estuvo marcado por la pandemia de COVID-19 y sus efectos en cadenas de suministro "
        "globales, seguido de un repunte inflacionario generalizado en 2021-2022 que afecto tanto a economias "
        "avanzadas (Estados Unidos) como emergentes (Peru, promedio regional de America Latina y el Caribe). "
        "Estados Unidos, ancla monetaria de Ecuador, paso de una inflacion de 1.23% en 2020 a 8.00% en 2022, la "
        "mayor variacion interanual de toda la serie analizada para ese pais, en un contexto de estimulo fiscal "
        "expansivo, cuellos de botella logisticos globales y posterior endurecimiento de la politica monetaria de "
        "la Reserva Federal. El promedio de America Latina y el Caribe siguio un patron similar, alcanzando 8.81% "
        "en 2022, el valor mas alto de toda la serie regional 2014-2024 utilizada en este estudio."
    )

    # Fuentes y metodologia
    pdf.add_page()
    h1(pdf, "7. Fuentes y Metodologia")
    body(
        pdf,
        "Fuente de datos: World Bank Open Data API (indicadores FP.CPI.TOTL.ZG, NY.GDP.MKTP.KD.ZG, "
        "SL.UEM.TOTL.ZS), consultada el 2026-07-16. Periodo: 2014-2024 (11 observaciones anuales). "
        "Paises/regiones: Ecuador, Estados Unidos, Peru, Panama, America Latina y el Caribe (excl. altos ingresos). "
        "Ver docs/fuentes.md y docs/metodologia.md para el detalle completo de trazabilidad."
    )

    # Arquitectura multiagentica
    h1(pdf, "8. Arquitectura Multiagentica")
    body(
        pdf,
        "El proyecto se desarrollo mediante un agente coordinador y ocho agentes especializados (fuentes, "
        "recopilacion de datos, validacion, analisis economico, econometria, visualizacion, redaccion y "
        "auditoria), apoyados por seis subagentes. Cada agente tiene un rol, objetivo, entradas y salidas "
        "explicitos, encadenados mediante dependencias declaradas en config/tasks.yaml: el resultado de un agente "
        "es la entrada verificable del siguiente, lo que distingue esta arquitectura de una simple sucesion de "
        "conversaciones independientes con una herramienta de inteligencia artificial. El detalle completo de "
        "cada agente y subagente, incluyendo el diagrama de flujo, se encuentra en "
        "docs/arquitectura_multiagente.md, config/agents.yaml, config/tasks.yaml y en el Anexo C de este informe. "
        "La bitacora de ejecucion, con fecha, tarea, archivos utilizados, resultado, errores encontrados y "
        "responsable humano de validacion, se registra en docs/bitacora_agentes.md."
    )

    # Procesamiento de datos
    h1(pdf, "9. Procesamiento de Datos")
    body(
        pdf,
        "Los datos crudos se descargaron mediante scripts/download_data.py y se conservaron sin alteracion en "
        "data/raw/. El Agente de Validacion (scripts/validate_data.py) reviso duplicados, completitud y valores "
        "atipicos, generando el dataset final en data/processed/inflacion_pib_desempleo.csv. El log de hallazgos "
        "esta disponible en outputs/logs/validation_log.md."
    )

    # Analisis estadistico / econometrico
    pdf.add_page()
    h1(pdf, "10. Analisis Estadistico y Econometrico")
    h2(pdf, "10.1 Estadistica descriptiva de la inflacion por pais")
    table(
        pdf,
        comparativos,
        col_widths=[45, 22, 24, 20, 20, 22, 21],
        headers=["Pais", "Prom. %", "Mediana %", "Min. %", "Max. %", "Desv.Est.", "CV %"],
    )
    body(
        pdf,
        "Interpretacion: Ecuador y Panama, ambas economias dolarizadas, presentan la inflacion promedio mas baja "
        "y menor dispersion del grupo, consistente con la hipotesis de que la dolarizacion actua como ancla "
        "nominal. Peru y la region LAC muestran mayor variabilidad, asociada a episodios de mayor inflacion en "
        "2022."
    )

    h2(pdf, "10.2 Comparacion pre y post pandemia (inflacion promedio, %)")
    table(pdf, pre_post, col_widths=[55, 45, 45], headers=["Pais", "2014-2019", "2020-2024"])
    body(
        pdf,
        "Interpretacion: Peru, Estados Unidos y el promedio de America Latina y el Caribe registraron un "
        "incremento marcado de la inflacion promedio en 2020-2024 respecto de 2014-2019, coincidiendo con el "
        "choque de oferta global post-pandemia. Panama registro un incremento leve. Ecuador, en cambio, muestra "
        "una inflacion promedio ligeramente MENOR en 2020-2024 (1.40%) que en 2014-2019 (1.62%): el efecto del "
        "pico de 2022 (3.47%) fue compensado, en el promedio del sub-periodo, por la deflacion de 2020 (-0.34%) y "
        "la baja inflacion de otros anos del sub-periodo. Esto sugiere que, en promedio multianual, Ecuador fue "
        "relativamente resiliente al choque inflacionario global, aunque no estuvo exento de el en el ano puntual "
        "de mayor impacto."
    )

    h2(pdf, "10.3 Volatilidad de la inflacion (2014-2024)")
    table(pdf, volatilidad, col_widths=[55, 45, 45], headers=["Pais", "Desv. Estandar", "Coef. Variacion %"])
    body(
        pdf,
        "Interpretacion: la menor volatilidad relativa (coeficiente de variacion) se observa en las economias "
        "dolarizadas, reforzando la lectura de que la perdida de politica monetaria propia se traduce, en la "
        "practica, en mayor previsibilidad de precios domesticos."
    )

    pdf.add_page()
    h2(pdf, "10.4 Correlacion entre inflacion, PIB y desempleo por pais")
    table(
        pdf,
        correlaciones,
        col_widths=[42, 12, 28, 22, 28, 22],
        headers=["Pais", "n", "Corr. Infl-PIB", "p-valor", "Corr. Infl-Desem.", "p-valor"],
    )
    body(
        pdf,
        "Interpretacion: los coeficientes de correlacion deben leerse con cautela dado el tamano de muestra "
        "reducido (n=11 anos por pais). Se reportan junto con su p-valor para evaluar significancia estadistica; "
        "correlaciones con p-valor superior a 0.05 no deben interpretarse como relaciones estadisticamente "
        "significativas."
    )

    h2(pdf, "10.5 Regresion lineal: inflacion de Ecuador explicada por la inflacion de EE.UU.")
    table(
        pdf,
        regresion,
        col_widths=[45, 12, 22, 25, 20, 22, 25],
        headers=["Modelo", "n", "Beta", "Intercepto", "R2", "p-valor", "Error Est."],
    )
    beta = regresion.iloc[0]["pendiente_beta"]
    r2 = regresion.iloc[0]["r_cuadrado"]
    pval = regresion.iloc[0]["p_valor"]
    body(
        pdf,
        f"Interpretacion: el coeficiente beta ({beta}) indica el cambio esperado en la inflacion de Ecuador ante "
        f"un incremento de un punto porcentual en la inflacion de Estados Unidos. El R2 ({r2}) indica la "
        f"proporcion de la variabilidad de la inflacion ecuatoriana explicada por la inflacion estadounidense. "
        f"Con un p-valor de {pval}, este resultado {'es' if pval < 0.05 else 'no es'} estadisticamente "
        f"significativo al 5%. Este modelo simple no controla por otras variables relevantes (precio del "
        f"petroleo, gasto publico, remesas) y debe interpretarse como evidencia exploratoria, no causal."
    )

    h2(pdf, "10.6 Visualizacion de resultados: dashboard interactivo")
    body(
        pdf,
        "El Agente de Visualizacion tradujo las tablas anteriores en un dashboard web (dashboard/), construido "
        "con Next.js y Recharts, desplegado publicamente en Vercel. El dashboard incluye: evolucion temporal de "
        "la inflacion por pais (grafico de lineas), comparacion de inflacion promedio (grafico de barras), "
        "relacion inflacion-PIB (grafico de dispersion), filtros interactivos por pais/ano/indicador, una tabla "
        "de datos completa y un parrafo de interpretacion economica bajo cada grafico -no se presentan graficos "
        "sin lectura interpretativa-. El detalle de los componentes y las reglas de diseño se documenta en "
        "subagents/charts_subagent.md."
    )

    # Resultados
    pdf.add_page()
    h1(pdf, "11. Resultados")
    body(
        pdf,
        "Los resultados confirman que Ecuador exhibe, en el periodo 2014-2024, la inflacion promedio mas baja "
        "y una de las volatilidades mas bajas del grupo de comparacion, patron compartido con Panama (la otra "
        "economia dolarizada de la muestra). El pico inflacionario de 2022 fue generalizado en las cinco "
        "entidades analizadas, coincidiendo con el choque de oferta post-pandemia y el alza de precios de "
        "materias primas a nivel global."
    )
    body(
        pdf,
        "En terminos de crecimiento del PIB (Anexo A), Panama registra la mayor volatilidad de toda la muestra "
        "(desviacion estandar de 8.36 puntos porcentuales), reflejo de su exposicion al comercio via el Canal de "
        "Panama y a flujos de inversion mas volatiles, pese a ser tambien una economia dolarizada de baja "
        "inflacion; esto ilustra que la dolarizacion estabiliza precios, pero no necesariamente el ciclo "
        "economico real. Ecuador, por su parte, muestra la tasa de desempleo promedio mas baja del grupo (4.02%), "
        "aunque este dato debe leerse considerando las particularidades de medicion del subempleo y la economia "
        "informal en el mercado laboral ecuatoriano, no capturadas por la tasa de desempleo abierto."
    )

    # Discusion
    h1(pdf, "12. Discusion")
    body(
        pdf,
        "La evidencia sobre niveles y volatilidad promedio es consistente con la literatura sobre economias "
        "dolarizadas: Ecuador y Panama, las dos economias sin politica monetaria propia de la muestra, muestran "
        "la inflacion mas baja y estable del grupo. Sin embargo, el modelo de regresion lineal simple entre la "
        "inflacion de Ecuador y la de Estados Unidos (seccion 10.5) no encuentra una relacion lineal fuerte ni "
        "estadisticamente significativa con datos anuales (n=11). Esto no descarta el mecanismo de inflacion "
        "importada descrito en el marco conceptual, pero si indica que, con la frecuencia y el tamano de muestra "
        "disponibles en este proyecto, no puede confirmarse una transmision lineal directa y contemporanea; un "
        "analisis con series mensuales y rezagos temporales seria necesario para probar esta hipotesis con mayor "
        "rigor."
    )
    body(
        pdf,
        "La correlacion positiva y estadisticamente significativa entre inflacion y crecimiento del PIB en "
        "Panama (r=0.754, p=0.007) es el hallazgo individual mas robusto de este estudio. Una lectura economica "
        "plausible es que, en una economia pequena y muy abierta como la panamena, los periodos de auge del "
        "comercio y la actividad portuaria elevan simultaneamente la demanda agregada y los precios domesticos; "
        "sin embargo, con una sola fuente de datos y sin controlar por terceras variables (precios de fletes, "
        "trafico del Canal), este resultado debe tratarse como una asociacion a profundizar, no como evidencia "
        "causal. Para Ecuador, Estados Unidos y Peru, ninguna de las correlaciones inflacion-PIB o "
        "inflacion-desempleo alcanza significancia estadistica al 5%, lo que es consistente con una curva de "
        "Phillips inestable o no lineal en el periodo analizado, tal como anticipa buena parte de la literatura "
        "macroeconomica reciente."
    )

    # Riesgos y oportunidades
    h1(pdf, "13. Riesgos y Oportunidades para Ecuador")
    h2(pdf, "Riesgos")
    for r in [
        "Dependencia de la politica monetaria de Estados Unidos sin capacidad de ajuste propio: decisiones de la "
        "Reserva Federal ajenas a la coyuntura ecuatoriana se transmiten igualmente a la economia domestica.",
        "Vulnerabilidad ante choques externos de precios de materias primas, en particular el petroleo, principal "
        "producto de exportacion del pais y determinante clave de los ingresos fiscales.",
        "Perdida de competitividad cambiaria frente a paises con moneda propia en episodios de apreciacion del "
        "dolar, que encarece las exportaciones ecuatorianas no petroleras en mercados con monedas depreciadas.",
        "Limitada capacidad de respuesta fiscal y monetaria conjunta ante una recesion importada, dado que el "
        "unico instrumento de ajuste disponible es la politica fiscal.",
    ]:
        bullet(pdf, r)
    h2(pdf, "Oportunidades")
    for o in [
        "Estabilidad de precios como atractivo para inversion extranjera directa de largo plazo, al reducir el "
        "riesgo cambiario percibido por inversionistas internacionales.",
        "Menor riesgo cambiario para el comercio exterior denominado en dolares, lo que simplifica la "
        "planificacion financiera de empresas exportadoras e importadoras.",
        "Anclaje de expectativas inflacionarias que favorece la planificacion economica de hogares y empresas, "
        "facilitando contratos y creditos a plazos mas largos.",
        "Menores costos de transaccion en el comercio con Estados Unidos, su principal socio comercial y fuente "
        "de remesas, al no existir riesgo de devaluacion frente a esa moneda.",
    ]:
        bullet(pdf, o)

    # Conclusiones
    pdf.add_page()
    h1(pdf, "14. Conclusiones")
    body(
        pdf,
        "La inflacion en Ecuador durante 2014-2024 fue comparativamente baja y estable frente a Peru, la region "
        "LAC y, en gran parte del periodo, frente a Estados Unidos. Esta evidencia respalda la hipotesis de que "
        "la dolarizacion actua como un ancla nominal efectiva, aunque el analisis tambien evidencia la "
        "transmision de choques inflacionarios externos (2022) hacia la economia ecuatoriana."
    )

    # Recomendaciones
    h1(pdf, "15. Recomendaciones")
    for rec in [
        "Fortalecer la disciplina fiscal como mecanismo de estabilizacion sustituto de la politica monetaria, "
        "dado que Ecuador no puede usar la tasa de interes ni el tipo de cambio para amortiguar choques.",
        "Diversificar el comercio exterior y la matriz productiva para reducir la exposicion a un unico ciclo "
        "monetario externo y a la volatilidad del precio del petroleo.",
        "Complementar este analisis con series mensuales oficiales de INEC/BCE para mayor granularidad temporal "
        "y poder aplicar modelos de series de tiempo con rezagos (ej. ARIMA, modelos de correccion de error).",
        "Monitorear de forma continua el diferencial de inflacion con Estados Unidos como indicador temprano de "
        "perdida o ganancia de competitividad real, dado el regimen cambiario fijo de facto.",
        "Ampliar el analisis a un panel de mas paises dolarizados o con caja de conversion (ej. Panama, El "
        "Salvador, Zimbabue) para robustecer las comparaciones sobre los efectos de renunciar a la politica "
        "monetaria propia.",
    ]:
        bullet(pdf, rec)

    # Limitaciones
    h1(pdf, "16. Limitaciones")
    for lim in [
        "Se utilizan series anuales (Banco Mundial); no se incorporan series mensuales oficiales de INEC/BCE.",
        "El tamano de muestra (n=11 anos) limita la robustez estadistica de correlaciones y regresiones.",
        "El modelo de regresion no controla por variables omitidas relevantes (petroleo, remesas, gasto publico).",
        "Trabajo de alcance individual adaptado del formato grupal original de la consigna.",
    ]:
        bullet(pdf, lim)

    # Referencias
    pdf.add_page()
    h1(pdf, "17. Referencias Bibliograficas")
    for ref in [
        "World Bank. (2026). Inflation, consumer prices (annual %) [Conjunto de datos]. https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG",
        "World Bank. (2026). GDP growth (annual %) [Conjunto de datos]. https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG",
        "World Bank. (2026). Unemployment, total (% of total labor force) [Conjunto de datos]. https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS",
        "Mundell, R. A. (1961). A theory of optimum currency areas. The American Economic Review, 51(4), 657-665.",
        "Banco Central del Ecuador. (2026). Cifras economicas del Ecuador. https://www.bce.fin.ec",
        "Instituto Nacional de Estadistica y Censos. (2026). Indice de Precios al Consumidor. https://www.ecuadorencifras.gob.ec",
    ]:
        bullet(pdf, ref)
        pdf.ln(1)

    # Anexos
    h1(pdf, "18. Anexos")
    h2(pdf, "Anexo A. Estadistica descriptiva completa por pais e indicador")
    INDICATOR_SHORT = {
        "inflacion_precios_consumidor": "Inflacion (%)",
        "crecimiento_pib": "Crec. PIB (%)",
        "tasa_desempleo": "Desempleo (%)",
    }
    descriptivas = descriptivas.copy()
    descriptivas["indicador"] = descriptivas["indicador"].map(INDICATOR_SHORT).fillna(descriptivas["indicador"])
    table(
        pdf,
        descriptivas,
        col_widths=[38, 28, 10, 18, 18, 20, 16, 16],
        headers=["Pais", "Indicador", "n", "Media", "Mediana", "Desv.Est.", "Min.", "Max."],
    )

    h2(pdf, "Anexo B. Numeros indice de inflacion, base 2014=100")
    body(
        pdf,
        "Numero indice construido acumulando (1 + tasa de inflacion anual / 100) desde 2014, para representar el "
        "crecimiento acumulado del nivel de precios en cada economia. Ver metodologia completa en "
        "scripts/calculate_indicators.py y el archivo outputs/tables/numeros_indice_inflacion.csv."
    )
    indice_final = pd.read_csv(TABLES_DIR / "numeros_indice_inflacion.csv")
    indice_2024 = indice_final[indice_final["anio"] == 2024][["pais", "numero_indice"]].sort_values("numero_indice")
    table(pdf, indice_2024, col_widths=[90, 84], headers=["Pais", "Indice de precios acumulado 2024 (2014=100)"])
    body(
        pdf,
        "Interpretacion: un valor de, por ejemplo, 115 significa que el nivel de precios acumulado del pais creceria "
        "un 15% entre 2014 y 2024 si se acumularan las tasas de inflacion anual reportadas. Los paises con menor "
        "numero indice final acumularon menos inflacion en la decada, consistente con los resultados de las "
        "secciones 10.1 y 10.3."
    )

    h2(pdf, "Anexo C. Glosario de agentes y subagentes")
    body(
        pdf,
        "Ver descripcion completa de cada agente y subagente en agents/*.md, subagents/*.md y "
        "docs/arquitectura_multiagente.md del repositorio. Resumen:"
    )
    for nombre, rol in [
        ("Coordinador", "Distribuye tareas, verifica coherencia entre agentes, consolida el analisis final."),
        ("Agente de Fuentes", "Localiza y verifica fuentes oficiales (Banco Mundial, BCE, INEC, FMI)."),
        ("Agente de Recopilacion de Datos", "Descarga y organiza los datos crudos con metadatos completos."),
        ("Agente de Validacion", "Revisa faltantes, duplicados, atipicos y consistencia de unidades."),
        ("Agente de Analisis Economico", "Calcula indicadores comparativos e interpreta tendencias."),
        ("Agente Econometrico/Estadistico", "Aplica estadistica descriptiva, correlacion, regresion y volatilidad."),
        ("Agente de Visualizacion", "Diseña graficos y tablas del dashboard."),
        ("Agente Redactor", "Elabora el informe academico final en PDF."),
        ("Agente Auditor", "Revisa trazabilidad, coherencia, estructura y ausencia de datos inventados."),
    ]:
        bullet(pdf, f"{nombre}: {rol}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PATH))
    print(f"[OK] Informe generado en {OUTPUT_PATH} ({pdf.page_no()} paginas)")


if __name__ == "__main__":
    build_pdf()
