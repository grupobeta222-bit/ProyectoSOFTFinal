import pathlib
import re

from src.infrastructure.ai.groq_client import GroqClient


class AgenteConversacional:

    def __init__(self, service, groq_client=None):
        self.service = service
        self.groq_client = groq_client or GroqClient()
        self.historial = []
        self.MAX_PAREJAS = 8

    def _contexto_catalogo(self):
        vehiculos = self.service.listar_vehiculos() or []
        planes = self.service.listar_planes() or []

        texto = "=== CATÁLOGO DE VEHÍCULOS ===\n"
        for v in vehiculos:
            texto += (
                f"- {v.id[:3]}-{v.id[3:]}: {v.marca} {v.modelo} {v.anio} | "
                f"Precio: ${v.precio_base:,.2f} | "
                f"Motor: {v.motor} | Transmisión: {v.transmision} | "
                f"Combustible: {v.combustible} | Stock: {v.stock}\n"
            )

        texto += "\n=== PLANES DE FINANCIAMIENTO ===\n"
        for p in planes:
            plazos = ", ".join(str(x) for x in p.plazos_disponibles)
            texto += (
                f"- {p.id[:4]}-{p.id[4:]}: {p.nombre} | "
                f"Entrada mínima: {p.entrada_minima_porcentaje}% | "
                f"Tasa anual: {p.tasa_anual}% | "
                f"Plazos: {plazos} meses | Comisión: ${p.comision_apertura:,.2f}\n"
            )

        return texto

    def _system_prompt(self):
        return (
            "Eres el asistente virtual de AutoVentas Pro, una concesionaria de vehículos en Ecuador. "
            "Respondes SIEMPRE en español, de forma amable y natural.\n\n"
            "INSTRUCCIONES:\n"
            "1. Responde directamente con la información. Incluye enlaces como:\n"
            "   <a href='/vehiculo/{id}'>Ver {marca} {modelo}</a> o\n"
            "   <a href='/cotizar?v={id}'>Cotizar</a>\n"
            "   También puedes redirigir a páginas del sitio:\n"
            "   /catalogo - Catálogo completo\n"
            "   /financiamiento - Planes de financiamiento\n"
            "   /contacto - Contacto y asesores\n"
            "   /login - Inicio de sesión\n"
            "2. Cuando menciones un vehículo, pon el ID primero: (VEH-001) Toyota Corolla, (VEH-002) Toyota RAV4. Si es un plan: (PLAN-001) Plan Clásico. Si preguntan características, dáselas completas (precio, motor, transmisión, combustible, stock).\n"
            "3. Si preguntan comparaciones, compáralos directamente en la conversación.\n"
            "4. Si el usuario quiere COTIZAR, guíalo paso a paso:\n"
            "   - ¿Qué vehículo le interesa?\n"
            "   - ¿Qué plan de financiamiento prefiere?\n"
            "   - ¿A cuántos meses?\n"
            "   - ¿Cuánto dará de entrada?\n"
            "   - Nombre, email, cédula y teléfono\n"
            "5. CUANDO TENGAS TODOS LOS DATOS necesarios, agrega al FINAL de tu respuesta:\n"
            "   [COTIZAR: vehiculo_id|plan_id|nombre|email|cedula|telefono|entrada|plazo]\n"
            "   Ejemplo: [COTIZAR: VEH-001|PLAN-001|María López|maria@mail.com|0912345678|0991234567|6000|24]\n"
            "6. No inventes vehículos ni planes. Usa solo la información del catálogo que te doy abajo.\n"
            "7. No te repitas ni saludes cada vez si ya están conversando.\n\n"
            + self._contexto_catalogo()
        )

    def procesar_entrada(self, texto):
        texto = (texto or "").strip()
        if not texto:
            return "Escribe algo para que pueda ayudarte."

        self.historial.append({"role": "user", "content": texto})
        if len(self.historial) > self.MAX_PAREJAS * 2:
            self.historial = self.historial[-(self.MAX_PAREJAS * 2):]

        try:
            respuesta = self.groq_client.conversar(self.historial, self._system_prompt())
        except Exception as e:
            return f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}"

        self.historial.append({"role": "assistant", "content": respuesta})
        if len(self.historial) > self.MAX_PAREJAS * 2:
            self.historial = self.historial[-(self.MAX_PAREJAS * 2):]

        resultado = self._procesar_cotizacion(respuesta)
        if resultado:
            return resultado

        return respuesta

    def _procesar_cotizacion(self, respuesta):
        match = re.search(r'\[COTIZAR:\s*(.*?)\]', respuesta)
        if not match:
            return None

        from src.interfaces.presentation.context import generar_cotizacion_segura

        texto_sin_marcador = respuesta.replace(match.group(0), "").strip()

        datos = match.group(1).split("|")
        if len(datos) < 8:
            return texto_sin_marcador + (
                "\n\nFaltan datos para generar la cotización. "
                "Por favor completa todos los campos."
            )

        vehiculo_id, plan_id, nombre, email, cedula, telefono, entrada, plazo = [
            x.strip().replace("$", "").replace(",", "").replace("-", "") for x in datos[:8]
        ]

        try:
            cotizacion, tabla, es_real = generar_cotizacion_segura(
                vehiculo_id=vehiculo_id,
                plan_id=plan_id,
                nombre_cliente=nombre,
                email_cliente=email,
                cedula_cliente=cedula,
                telefono_cliente=telefono,
                entrada=float(entrada),
                plazo_meses=int(plazo),
            )

            from src.interfaces.presentation.pdf_cotizacion import generar_pdf_cotizacion

            pdf_bytes = generar_pdf_cotizacion(cotizacion, tabla)
            pdf_dir = pathlib.Path(__file__).resolve().parent / "assets" / "pdfs"
            pdf_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = pdf_dir / f"{cotizacion.id}.pdf"
            pdf_path.write_bytes(pdf_bytes)

            resumen = (
                f"{texto_sin_marcador}\n\n"
                f"✅ Cotización generada exitosamente\n"
                f"📋 ID: {cotizacion.id}\n"
                f"💰 Cuota mensual: ${cotizacion.cuota_mensual:,.2f}\n"
                f"📊 Total financiado: ${cotizacion.monto_financiado:,.2f}\n"
                f"📄 "
                f'<a href="/assets/pdfs/{cotizacion.id}.pdf" '
                f'style="color:#e74c3c;font-weight:bold;" download>Descargar PDF</a>'
            )
            return resumen

        except Exception as e:
            return texto_sin_marcador + (
                f"\n\nNo se pudo generar la cotización: {str(e)}"
            )
