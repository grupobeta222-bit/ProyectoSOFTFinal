from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from src.interfaces.presentation.helpers import money as _money


def _estado(c):
    return str(getattr(c, "estado", "pendiente") or "pendiente").strip().lower().replace(" ", "_").replace("-", "_")


def generar_pdf_reporte(cotizaciones, ranking, filtros):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.3 * cm,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AutoVentas Pro", styles["Title"]))
    story.append(Paragraph("Reporte gerencial", styles["Heading2"]))
    story.append(Spacer(1, 8))

    texto_filtros = filtros or "Sin filtros aplicados"
    story.append(Paragraph("Filtros: " + texto_filtros, styles["Normal"]))
    story.append(Spacer(1, 12))

    total_cots = len(cotizaciones)
    ventas = [c for c in cotizaciones if _estado(c) == "cerrada"]
    ingreso = sum(float(getattr(c, "precio_vehiculo", 0) or 0) for c in ventas)
    cerradas = len(ventas)
    tasa = round((cerradas / total_cots) * 100, 2) if total_cots else 0

    kpis = [
        ["Indicador", "Valor"],
        ["Cotizaciones", str(total_cots)],
        ["Ventas cerradas", str(cerradas)],
        ["Tasa de cierre", str(tasa) + "%"],
        ["Ingreso por ventas", _money(ingreso)],
    ]
    tabla_kpi = Table(kpis, colWidths=[7 * cm, 8 * cm])
    tabla_kpi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e63946")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tabla_kpi)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Ranking de asesores", styles["Heading2"]))
    datos_ranking = [["Asesor", "Cotizaciones", "Cerradas", "Valor", "Rating"]]
    for r in ranking:
        datos_ranking.append([
            r.get("nombre", ""),
            str(r.get("cotizaciones", 0)),
            str(r.get("cerradas", 0)),
            _money(r.get("valor", 0)),
            str(r.get("rating", "")),
        ])
    if len(datos_ranking) == 1:
        datos_ranking.append(["Sin datos", "0", "0", "$0.00", "-"])
    tabla_ranking = Table(datos_ranking, repeatRows=1, colWidths=[6 * cm, 2.5 * cm, 2.5 * cm, 3 * cm, 2 * cm])
    tabla_ranking.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tabla_ranking)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Cotizaciones", styles["Heading2"]))
    datos = [["ID", "Cliente", "Vehículo", "Plan", "Cuota", "Estado"]]
    for c in cotizaciones[:25]:
        datos.append([
            getattr(c, "id", ""),
            getattr(c, "nombre_cliente", ""),
            getattr(c, "vehiculo_id", ""),
            getattr(c, "plan_id", ""),
            _money(getattr(c, "cuota_mensual", 0)),
            _estado(c),
        ])
    if len(datos) == 1:
        datos.append(["Sin registros", "", "", "", "", ""])
    tabla = Table(datos, repeatRows=1, colWidths=[2.5 * cm, 4 * cm, 2.5 * cm, 2.6 * cm, 2.8 * cm, 2.4 * cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e63946")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("PADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(tabla)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
