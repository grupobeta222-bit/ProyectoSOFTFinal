from collections import Counter


class DashboardService:
    def __init__(self, cotizacion_repo, usuario_repo):
        self.cotizacion_repo = cotizacion_repo
        self.usuario_repo = usuario_repo

    def resumen(self, cotizaciones=None):
        cotizaciones = cotizaciones if cotizaciones is not None else self.cotizacion_repo.find_all()
        estados = Counter(item.estado for item in cotizaciones)
        ventas = [item for item in cotizaciones if item.estado == "cerrada"]
        return {
            "total": len(cotizaciones),
            "pendientes": estados["pendiente"],
            "en_revision": estados["en_revision"],
            "aprobadas": estados["aprobada"],
            "rechazadas": estados["rechazada"],
            "cerradas": len(ventas),
            "ingresos": round(sum(item.precio_vehiculo for item in ventas), 2),
            "comisiones": round(sum(item.comision_apertura for item in ventas), 2),
        }

    def ranking(self, cotizaciones=None):
        cotizaciones = cotizaciones if cotizaciones is not None else self.cotizacion_repo.find_all()
        filas = []
        for asesor in self.usuario_repo.find_asesores():
            asignadas = [item for item in cotizaciones if item.asesor_id == asesor.id]
            ventas = [item for item in asignadas if item.estado == "cerrada"]
            filas.append({
                "id": asesor.id,
                "nombre": asesor.nombre,
                "cotizaciones": len(asignadas),
                "cerradas": len(ventas),
                "valor": round(sum(item.precio_vehiculo for item in ventas), 2),
                "rating": asesor.rating,
            })
        return sorted(filas, key=lambda fila: (fila["cerradas"], fila["valor"]), reverse=True)
