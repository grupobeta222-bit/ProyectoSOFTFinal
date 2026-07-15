from src.interfaces.presentation.context import ui


def render_amortizacion_table(tabla):
    filas = "".join(
        f'<tr><td>{f["cuota"]}</td>'
        f'<td>${f["saldo_inicial"]:,.2f}</td>'
        f'<td>${f["capital"]:,.2f}</td>'
        f'<td>${f["interes"]:,.2f}</td>'
        f'<td>${f["cuota_total"]:,.2f}</td>'
        f'<td>${f["saldo_final"]:,.2f}</td></tr>'
        for f in tabla
    )
    total_capital = sum(f["capital"] for f in tabla)
    total_interes = sum(f["interes"] for f in tabla)
    total_pagado = sum(f["cuota_total"] for f in tabla)
    filas += (
        '<tr style="font-weight:900;background:#1b1b1b;">'
        '<td>Total</td><td></td>'
        f'<td>${total_capital:,.2f}</td>'
        f'<td>${total_interes:,.2f}</td>'
        f'<td>${total_pagado:,.2f}</td>'
        '<td></td></tr>'
    )
    ui.html(
        '<div class="av-cot-card">'
        '<div class="av-cot-step-title">Tabla de amortización</div>'
        '<div style="color:#777;font-size:13px;margin-bottom:12px;">Detalle de capital, interés y saldo por cada cuota.</div>'
        '<div class="av-tabla-wrap"><table>'
        '<thead><tr><th>#</th><th>Saldo Inicial</th><th>Capital</th><th>Interés</th><th>Cuota Total</th><th>Saldo Final</th></tr></thead>'
        f'<tbody>{filas}</tbody>'
        '</table></div></div>'
    )
