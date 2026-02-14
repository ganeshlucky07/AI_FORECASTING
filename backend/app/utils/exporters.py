from io import BytesIO
from typing import Iterable, List, Mapping

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def rows_to_excel(
    rows: Iterable[Mapping],
    columns: List[str],
) -> BytesIO:
    """
    Helper: convert an iterable of dict-like rows to an in-memory Excel file.

    - `rows`: iterable of mappings (e.g. dicts) whose keys match `columns`
    - `columns`: explicit column ordering for the Excel sheet
    """
    df = pd.DataFrame(list(rows), columns=columns)
    output = BytesIO()
    # Use xlsxwriter or openpyxl (pandas selects an available engine).
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)
    return output


def simple_table_pdf(
    title: str,
    headers: List[str],
    rows: Iterable[Iterable[str]],
) -> BytesIO:
    """
    Helper: build a very simple PDF with a title and a table-like listing.

    This is intentionally minimal so you can later swap it with a richer
    reporting system (e.g. templated HTML to PDF).
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 30

    # Header row
    c.setFont("Helvetica-Bold", 10)
    header_text = " | ".join(headers)
    c.drawString(40, y, header_text)
    y -= 20

    c.setFont("Helvetica", 9)
    for row in rows:
        line = " | ".join(str(cell) for cell in row)
        if y < 40:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)
        c.drawString(40, y, line)
        y -= 14

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

