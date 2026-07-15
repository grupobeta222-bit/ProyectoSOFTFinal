class NotificacionService:
    MENSAJES = {
        "pendiente": "Cotización pendiente de revisión",
        "en_revision": "Cotización lista para decisión",
        "aprobada": "Cotización aprobada pendiente de cierre",
    }

    def listar(self, cotizaciones, rol, asesor_id=None):
        resultado = []
        for cotizacion in cotizaciones:
            if rol == "asesor" and cotizacion.asesor_id != asesor_id:
                continue
            if cotizacion.estado in self.MENSAJES:
                resultado.append({
                    "id": cotizacion.id,
                    "estado": cotizacion.estado,
                    "mensaje": self.MENSAJES[cotizacion.estado],
                })
        return resultado
