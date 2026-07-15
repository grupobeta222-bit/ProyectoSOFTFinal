from src.interfaces.presentation.context import ui, get_clientes, get_cotizaciones
from src.interfaces.presentation.components.admin_layout import admin_shell, admin_title


def admin_clientes():
    content = admin_shell('clientes')
    if content is None:
        return

    clientes = get_clientes() or []
    cotizaciones = get_cotizaciones() or []

    rows = []
    if clientes:
        for cliente in clientes:
            clave = getattr(cliente, 'cedula', '') or getattr(cliente, 'email', '')
            total = 0
            for c in cotizaciones:
                clave_cot = getattr(c, 'cedula_cliente', '') or getattr(c, 'email_cliente', '')
                if clave_cot == clave:
                    total += 1
            rows.append({
                'nombre': getattr(cliente, 'nombre', ''),
                'cedula': getattr(cliente, 'cedula', ''),
                'email': getattr(cliente, 'email', ''),
                'telefono': getattr(cliente, 'telefono', ''),
                'ciudad': getattr(cliente, 'ciudad', ''),
                'cotizaciones': total,
            })
    elif cotizaciones:
        vistos = {}
        for cot in cotizaciones:
            clave = getattr(cot, 'cedula_cliente', '') or getattr(cot, 'email_cliente', '')
            if clave not in vistos:
                vistos[clave] = {
                    'nombre': getattr(cot, 'nombre_cliente', ''),
                    'cedula': getattr(cot, 'cedula_cliente', ''),
                    'email': getattr(cot, 'email_cliente', ''),
                    'telefono': getattr(cot, 'telefono_cliente', ''),
                    'ciudad': getattr(cot, 'ciudad_cliente', ''),
                    'cotizaciones': 0,
                }
            vistos[clave]['cotizaciones'] += 1
        rows = list(vistos.values())

    with content:
        ui.html(admin_title('Clientes registrados', 'Clientes generados desde el proceso de cotización.'))
        with ui.card().style(
            'background:#141414;border:1px solid #242424;border-radius:22px;'
            'padding:26px;color:#fff;width:100%;'
        ):
            ui.html('<h2 style="font-size:20px;color:#fff;margin:0 0 18px;">Listado de clientes</h2>')
            if not rows:
                ui.html('<div style="color:#aaa;font-size:14px;">Todavía no hay clientes registrados.</div>')
                return
            filas = ""
            for r in rows:
                filas += (
                    f"<tr><td>{r['nombre']}</td><td>{r['cedula']}</td>"
                    f"<td>{r['email']}</td><td>{r['telefono']}</td>"
                    f"<td>{r['ciudad']}</td><td>{r['cotizaciones']}</td></tr>"
                )
            ui.html(f'''
            <div style="overflow-x:auto;width:100%;">
              <table class="av-admin-table">
                <thead>
                  <tr><th>Nombre</th><th>Cédula</th><th>Email</th>
                      <th>Teléfono</th><th>Ciudad</th><th>Cotizaciones</th></tr>
                </thead>
                <tbody>{filas}</tbody>
              </table>
            </div>
            ''')
