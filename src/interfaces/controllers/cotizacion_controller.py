from src.domain.exceptions.domain_exception import DomainException


class CotizacionController:

    def __init__(self, cotizacion_service):
        self.servicio = cotizacion_service

    def listar_vehiculos(self):
        vehiculos = self.servicio.listar_vehiculos()

        print("\n" + "=" * 70)
        print("  CATALOGO DE VEHICULOS")
        print("=" * 70)

        if not vehiculos:
            print("  No hay vehiculos disponibles.")
        else:
            for v in vehiculos:
                if v.tiene_stock():
                    disponible = "Disponible"
                else:
                    disponible = "Sin stock"

                print(
                    "  [" + v.id + "] " +
                    v.marca + " " + v.modelo + " " + str(v.anio) +
                    " | Motor: " + v.motor +
                    " | " + v.transmision +
                    " | " + v.combustible +
                    " | $" + str(v.precio_base) +
                    " | Stock: " + str(v.stock) +
                    " | " + disponible
                )

        print("=" * 70)
        return vehiculos

    def listar_planes(self):
        planes = self.servicio.listar_planes()

        print("\n" + "=" * 70)
        print("  PLANES DE FINANCIAMIENTO")
        print("=" * 70)

        if not planes:
            print("  No hay planes disponibles.")
        else:
            for p in planes:
                plazos = ", ".join(str(x) for x in p.plazos_disponibles)
                print(
                    "  [" + p.id + "] " + p.nombre +
                    " | Entrada min: " + str(p.entrada_minima_porcentaje) + "%" +
                    " | Tasa: " + str(p.tasa_anual) + "%" +
                    " | Plazos: " + plazos + " meses" +
                    " | Comision: $" + str(p.comision_apertura)
                )

        print("=" * 70)
        return planes

    def generar_cotizacion(self, vehiculo_id, plan_id,
                           nombre_cliente, email_cliente,
                           entrada, plazo_meses,
                           cedula_cliente="", telefono_cliente=""):
        try:
            cotizacion = self.servicio.generar_cotizacion(
                vehiculo_id      = vehiculo_id,
                plan_id          = plan_id,
                nombre_cliente   = nombre_cliente,
                email_cliente    = email_cliente,
                cedula_cliente   = cedula_cliente,
                telefono_cliente = telefono_cliente,
                entrada          = entrada,
                plazo_meses      = plazo_meses,
            )

            print("\n" + "=" * 70)
            print("  COTIZACION GENERADA EXITOSAMENTE")
            print("=" * 70)
            print("  ID            : " + cotizacion.id)
            print("  Estado        : " + cotizacion.estado)
            print("  Fecha         : " + cotizacion.fecha)
            print("  Cliente       : " + cotizacion.nombre_cliente + " (" + cotizacion.email_cliente + ")")
            print("  Cedula        : " + cotizacion.cedula_cliente)
            print("  Vehiculo ID   : " + cotizacion.vehiculo_id)
            print("  Plan ID       : " + cotizacion.plan_id)
            print("  Precio        : $" + str(cotizacion.precio_vehiculo))
            print("  Entrada       : $" + str(cotizacion.entrada))
            print("  Monto finan.  : $" + str(cotizacion.monto_financiado))
            print("  Tasa anual    : " + str(cotizacion.tasa_anual) + "%")
            print("  Plazo         : " + str(cotizacion.plazo_meses) + " meses")
            print("  Cuota mensual : $" + str(cotizacion.cuota_mensual))
            print("=" * 70)

            return cotizacion

        except DomainException as e:
            print("\n  [ERROR] " + str(e))
            raise

    def ver_tabla_amortizacion(self, cotizacion_id):
        try:
            resultado = self.servicio.obtener_tabla_amortizacion(cotizacion_id)
            tabla     = resultado["tabla_amortizacion"]

            print("\n" + "=" * 80)
            print("  TABLA DE AMORTIZACION - " + cotizacion_id)
            print("=" * 80)
            print("  {:>5}  {:>14}  {:>12}  {:>12}  {:>12}  {:>12}".format(
                "#", "Saldo Inicial", "Capital", "Interes", "Cuota Total", "Saldo Final"
            ))
            print("  " + "-" * 74)

            for fila in tabla:
                print("  {:>5}  ${:>13,.2f}  ${:>11,.2f}  ${:>11,.2f}  ${:>11,.2f}  ${:>11,.2f}".format(
                    fila["cuota"],
                    fila["saldo_inicial"],
                    fila["capital"],
                    fila["interes"],
                    fila["cuota_total"],
                    fila["saldo_final"],
                ))

            print("=" * 80)
            return resultado

        except DomainException as e:
            print("\n  [ERROR] " + str(e))
            raise

    def listar_cotizaciones(self):
        cotizaciones = self.servicio.listar_cotizaciones()

        print("\n" + "=" * 70)
        print("  COTIZACIONES REGISTRADAS")
        print("=" * 70)

        if not cotizaciones:
            print("  No hay cotizaciones registradas.")
        else:
            for c in cotizaciones:
                print("  " + str(c))

        print("=" * 70)
        return cotizaciones

    def cambiar_estado_cotizacion(self, cotizacion_id, nuevo_estado):
        try:
            cotizacion = self.servicio.cambiar_estado_cotizacion(cotizacion_id, nuevo_estado)
            print("  Estado actualizado: " + cotizacion.id + " -> " + cotizacion.estado)
            return cotizacion
        except DomainException as e:
            print("\n  [ERROR] " + str(e))
            raise

