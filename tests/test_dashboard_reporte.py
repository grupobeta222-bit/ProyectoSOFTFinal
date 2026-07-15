from src.domain.entities.cotizacion import Cotizacion
from src.interfaces.presentation.pdf_reporte import generar_pdf_reporte


def test_reporte_pdf_dashboard_se_genera():
    cot = Cotizacion(
        id="COT-TEST",
        vehiculo_id="VEH001",
        plan_id="PLAN001",
        nombre_cliente="Cliente Prueba",
        email_cliente="cliente@test.com",
        precio_vehiculo=25000,
        entrada=5000,
        plazo_meses=12,
        tasa_anual=12.5,
        asesor_id=1,
    )
    ranking = [{
        "nombre": "Josué Reyes Villón",
        "cotizaciones": 1,
        "cerradas": 0,
        "valor": 100,
        "rating": 4.8,
    }]

    pdf = generar_pdf_reporte([cot], ranking, "Sin filtros")

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
