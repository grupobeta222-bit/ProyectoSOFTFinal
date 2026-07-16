# AutoVentas Pro

Proyecto académico de una concesionaria desarrollado con Python, NiceGUI, SQLAlchemy y SQLite. Permite consultar el catálogo, generar cotizaciones con sistema francés, descargar PDF, administrar estados, revisar indicadores y exportar reportes.

## Ejecución limpia

Requiere Python 3.11 o superior y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python run_ui.py
```

Abrir `http://127.0.0.1:8080`. La base `autoventas.db` se crea automáticamente con vehículos, planes, cinco asesores y cotizaciones demo de los últimos tres meses.

## Despliegue en Render

Configurar el servicio con estos comandos:

```text
Build Command: pip install -r requirements.txt
Start Command: python -m src.interfaces.presentation.app_ui
```

La aplicación escucha en `0.0.0.0` y utiliza automáticamente el puerto definido por Render.

Pruebas:

```bash
uv run pytest -q
```

## Credenciales académicas

| Rol | Correo | Contraseña |
|---|---|---|
| Gerente | `admin@autoventas.com` | `Admin123` |
| Asesor | `asesor1@autoventas.com` | `Asesor123` |
| Cliente | `cliente1@demo.com` | `Cliente123` |

También existen `asesor2@autoventas.com` hasta `asesor5@autoventas.com`, con la misma contraseña de asesor. En SQLite solo se guardan hashes de las contraseñas.

## Reglas principales

- Flujo: `pendiente → en_revision → aprobada → cerrada`; `rechazada` es una salida final.
- El asesor asignado envía a revisión y puede cerrar una cotización aprobada.
- El gerente aprueba o rechaza las cotizaciones en revisión y puede cerrar una venta aprobada.
- Solo `cerrada` cuenta como venta.
- Ingreso = precio total del vehículo vendido.
- Comisión = comisión de apertura del plan guardada en la cotización.
- La cuota mensual no se registra como ingreso.

## Arquitectura

```text
src/domain          Entidades y reglas de negocio
src/application     Casos de uso, servicios y fábrica de cotización
src/infrastructure  ORM, SQLite, seguridad y repositorios
src/interfaces      Páginas NiceGUI, componentes, PDF y Excel
```

Las páginas principales o con estado usan clases (`HomePage`, `CotizacionPage`, `AsistentePage`, `LoginPage`, `ClienteLoginPage`, `AdminDashboardPage` y `AdminCotizacionesPage`). Las rutas conservan funciones pequeñas que crean y renderizan cada página.

## Contacto US-007

Responsable: Nick Olives.

- WhatsApp: `+593 98 669 8212`
- Correo: `grupobeta222@gmail.com`

Los botones abren WhatsApp y el cliente de correo; no envían mensajes automáticamente.

## Asistente

Necesita internet durante la demostración. Si no hay conexión, la página muestra un mensaje controlado y el resto del sistema continúa funcionando. La integración con Groq se conservó sin cambios por decisión del equipo. En `agente_cli.py` solo se ajustaron las instrucciones para mostrar primero los identificadores de vehículos y planes.

## Responsables principales

| Responsable | Área principal |
|---|---|
| Josué Reyes Villón | Dashboard, filtros y reportes |
| José Reyes Pazos | Cotización, cuotas y amortización |
| Cristel Chancay Ávila | Catálogo y vehículos |
| Kristel Bonilla Navarro | Clientes, accesos y roles |
| Nick Olives | Landing, responsive, contacto y testimonios |
