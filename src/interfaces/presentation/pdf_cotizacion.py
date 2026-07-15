from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from src.interfaces.presentation.helpers import money as _money


def generar_pdf_cotizacion(cotizacion, tabla):
    """Crea un PDF sencillo para la cotización.

    Se usa ReportLab porque es fácil de explicar: armamos una lista de
    elementos y luego la guardamos en memoria para descargarla.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.3*cm, bottomMargin=1.3*cm)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AutoVentas Pro", styles["Title"]))
    story.append(Paragraph("Cotización financiera - Sistema Francés", styles["Heading2"]))
    story.append(Spacer(1, 10))

    datos = [
        ["Cotización", cotizacion.id],
        ["Cliente", cotizacion.nombre_cliente],
        ["Cédula", cotizacion.cedula_cliente or "-"],
        ["Correo", cotizacion.email_cliente],
        ["Teléfono", cotizacion.telefono_cliente or "-"],
        ["Ciudad", cotizacion.ciudad_cliente or "-"],
        ["Vehículo", cotizacion.vehiculo_id],
        ["Plan", cotizacion.plan_id],
        ["Precio", _money(cotizacion.precio_vehiculo)],
        ["Entrada", _money(cotizacion.entrada)],
        ["Monto financiado", _money(cotizacion.monto_financiado)],
        ["Plazo", str(cotizacion.plazo_meses) + " meses"],
        ["Tasa anual", str(cotizacion.tasa_anual) + "%"],
        ["Cuota mensual", _money(cotizacion.cuota_mensual)],
    ]
    tabla_resumen = Table(datos, colWidths=[4*cm, 12*cm])
    tabla_resumen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tabla_resumen)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Tabla de amortización", styles["Heading2"]))
    datos_tabla = [["#", "Saldo inicial", "Capital", "Interés", "Cuota", "Saldo final"]]
    for fila in tabla:
        datos_tabla.append([
            fila["cuota"],
            _money(fila["saldo_inicial"]),
            _money(fila["capital"]),
            _money(fila["interes"]),
            _money(fila["cuota_total"]),
            _money(fila["saldo_final"]),
        ])

    total_capital = sum(f["capital"] for f in tabla)
    total_interes = sum(f["interes"] for f in tabla)
    total_pagado = sum(f["cuota_total"] for f in tabla)
    datos_tabla.append(["TOTAL", "", _money(total_capital), _money(total_interes), _money(total_pagado), ""])

    tabla_pdf = Table(datos_tabla, repeatRows=1, colWidths=[1.2*cm, 3*cm, 2.7*cm, 2.7*cm, 2.7*cm, 3*cm])
    tabla_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e63946")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f2f2f2")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tabla_pdf)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

