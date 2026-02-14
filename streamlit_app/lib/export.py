"""Export helpers for Excel and PDF (Streamlit app)."""
from io import BytesIO
from typing import Iterable, List, Mapping

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def rows_to_excel(rows: Iterable[Mapping], columns: List[str]) -> BytesIO:
    df = pd.DataFrame(list(rows), columns=columns)
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    buf.seek(0)
    return buf


def simple_table_pdf(
    title: str,
    headers: List[str],
    rows: Iterable[Iterable],
) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, " | ".join(headers))
    y -= 20
    c.setFont("Helvetica", 9)
    for row in rows:
        if y < 40:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)
        c.drawString(40, y, " | ".join(str(cell) for cell in row))
        y -= 14
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
