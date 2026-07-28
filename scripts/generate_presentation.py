"""Agente Redactor (apoyo).

Genera una presentacion breve en PDF (docs/presentacion_resultados.pdf) con
los hallazgos principales del proyecto, para la entrega y defensa oral.
Reproducible: solo requiere fpdf2 (pip), igual que generate_report.py.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "outputs" / "tables"
CHARTS_DIR = ROOT / "outputs" / "charts"
OUTPUT_PATH = ROOT / "docs" / "presentacion_resultados.pdf"

MARGIN = 15

# Enlaces por integrante, para generar una version personalizada de la
# diapositiva final segun quien vaya a presentar/entregar el documento.
ENLACES = {
    "christopher": {
        "repo": "github.com/christopherrobertog/analisis-contexto-nacional",
        "vercel": "analisis-contexto-nacional.vercel.app",
    },
    "maritza": {
        "repo": "github.com/maritzaaguinda8564-a11y/analisis-contexto--nacional",
        "vercel": "analisis-contexto-nacional-two.vercel.app",
    },
}


class SlidePDF(FPDF):
    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, f"{self.page_no()}/{{nb}}", align="R")


def title_slide(pdf: SlidePDF, kicker: str, title: str) -> None:
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 8, kicker.upper())
    pdf.ln(14)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 15, 15)
    pdf.multi_cell(0, 11, title)
    pdf.ln(4)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(MARGIN, pdf.get_y(), pdf.w - MARGIN, pdf.get_y())
    pdf.ln(8)


def bullet(pdf: SlidePDF, text: str, size: float = 13) -> None:
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 7.5, f"-  {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)


def load_table(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES_DIR / name)


def build_pdf(quien: str = "christopher", output_path: Path | None = None) -> None:
    enlaces = ENLACES[quien]
    output_path = output_path or OUTPUT_PATH
    pdf = SlidePDF(orientation="L", format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(MARGIN, 14, MARGIN)
    pdf.alias_nb_pages()

    comparativos = load_table("indicadores_comparativos.csv")
    regresion = load_table("regresion_ecuador_eeuu.csv")

    # 1. Portada
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(15, 15, 15)
    pdf.multi_cell(0, 13, "La inflacion en Ecuador (2014-2024)\nfrente al contexto internacional", align="C")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 14)
    pdf.multi_cell(0, 8, "Presentacion breve de resultados", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        0, 6,
        "Economia - Octavo Semestre | Analisis del Contexto Nacional y Global\n"
        "Christopher Guillen Aldas | Maritza Aguinda Alvarado",
        align="C",
    )

    # 2. Problema y objetivo
    title_slide(pdf, "El problema", "Una economia dolarizada, sin politica monetaria propia")
    bullet(pdf, "Ecuador adopto el dolar como moneda oficial en el ano 2000: no controla su tasa de interes ni su tipo de cambio.")
    bullet(pdf, "Pregunta: ¿como se ha comportado su inflacion (2014-2024) frente a economias de referencia, y cuanto depende de choques externos?")
    bullet(pdf, "Comparacion con Estados Unidos (ancla monetaria), Peru (moneda propia), Panama (tambien dolarizada) y America Latina y el Caribe.")

    # 3. Arquitectura
    title_slide(pdf, "Como se hizo", "Arquitectura multiagentica")
    bullet(pdf, "1 agente coordinador + 8 agentes especializados + 6 subagentes (fuentes, datos, validacion, analisis, econometria, visualizacion, redaccion, auditoria).")
    bullet(pdf, "Cada agente recibe una entrada verificable del anterior y entrega una salida trazable (config/tasks.yaml).")
    bullet(pdf, "Fuente de datos: World Bank Open Data API (inflacion, PIB, desempleo), consultada el 2026-07-16.")

    # 4. Resultados clave - tabla
    title_slide(pdf, "Resultados", "Inflacion promedio y volatilidad, 2014-2024")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(230, 230, 230)
    headers = ["Pais", "Promedio %", "Mediana %", "Min %", "Max %", "Desv.Est.", "CV %"]
    widths = [55, 30, 30, 25, 25, 30, 25]
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 9)
    for _, row in comparativos.iterrows():
        for val, w in zip(row, widths):
            text = f"{val:.2f}" if isinstance(val, float) else str(val)
            pdf.cell(w, 7, text, border=1, align="C")
        pdf.ln()
    pdf.ln(6)
    bullet(pdf, "Ecuador y Panama (dolarizadas) muestran la inflacion mas baja y menos volatil del grupo.", size=12)

    # 5. Grafico evolucion
    title_slide(pdf, "Evolucion temporal", "Inflacion de precios al consumidor, 2014-2024")
    img_path = CHARTS_DIR / "evolucion_inflacion.png"
    if img_path.exists():
        pdf.image(str(img_path), x=MARGIN + 20, y=pdf.get_y(), w=pdf.w - 2 * MARGIN - 40)

    # 6. Grafico dispersion
    title_slide(pdf, "Inflacion y crecimiento", "Inflacion vs. crecimiento del PIB, 2014-2024")
    img_path2 = CHARTS_DIR / "inflacion_vs_pib.png"
    if img_path2.exists():
        pdf.image(str(img_path2), x=MARGIN + 20, y=pdf.get_y(), w=pdf.w - 2 * MARGIN - 40)

    # 7. Hallazgo destacado
    title_slide(pdf, "Hallazgo principal", "¿Se confirma la 'inflacion importada'?")
    r2 = regresion.iloc[0]["r_cuadrado"]
    pval = regresion.iloc[0]["p_valor"]
    bullet(pdf, f"Regresion lineal Ecuador ~ Estados Unidos (2014-2024): R2 = {r2:.3f}, p-valor = {pval:.3f}.")
    bullet(pdf, "La evidencia de este periodo NO respalda una transmision lineal fuerte y directa entre ambas series, pese a compartir la misma moneda.")
    bullet(pdf, "Posibles razones: agregacion anual que oculta rezagos de corto plazo, subsidios fiscales a combustibles que amortiguan el traspaso, y tamano de muestra reducido (n=11).")

    # 8. Conclusiones
    title_slide(pdf, "Para cerrar", "Conclusiones y recomendaciones")
    bullet(pdf, "La dolarizacion actua como ancla nominal de precios, pero no es un mecanismo automatico: la disciplina fiscal (subsidios, gasto publico) tambien explica la baja inflacion observada.")
    bullet(pdf, "Riesgo principal: perder el espacio fiscal que amortigua los choques externos, sin tener politica monetaria propia como alternativa.")
    bullet(pdf, "Recomendacion: complementar este analisis con series mensuales oficiales (INEC/BCE) y modelos con rezagos para probar la hipotesis de inflacion importada con mayor rigor.")

    # 9. Enlaces
    title_slide(pdf, "Enlaces", "Producto entregado")
    bullet(pdf, f"Repositorio GitHub: {enlaces['repo']}", size=13)
    bullet(pdf, f"Dashboard en Vercel: {enlaces['vercel']}", size=13)
    bullet(pdf, "Informe completo en PDF: docs/informe_final.pdf", size=13)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    print(f"[OK] Presentacion generada en {output_path} ({pdf.page_no()} paginas)")


if __name__ == "__main__":
    import sys

    quien = sys.argv[1] if len(sys.argv) > 1 else "christopher"
    output_path = ROOT / "docs" / (
        "presentacion_resultados.pdf" if quien == "christopher" else f"presentacion_resultados_{quien}.pdf"
    )
    build_pdf(quien=quien, output_path=output_path)
