def money(valor):
    try:
        return f"${float(valor):,.2f}"
    except Exception:
        return "$0.00"


def estado_normalizado(estado):
    texto = str(estado or "pendiente").strip().lower()
    texto = texto.replace(" ", "_").replace("-", "_")
    estados = {
        "pendiente": "pendiente",
        "en_revision": "en_revision",
        "en_revisión": "en_revision",
        "revision": "en_revision",
        "revisión": "en_revision",
        "aprobada": "aprobada",
        "aprobado": "aprobada",
        "rechazada": "rechazada",
        "rechazado": "rechazada",
        "cerrada": "cerrada",
        "cerrado": "cerrada",
    }
    return estados.get(texto, "pendiente")


def estado_texto(estado):
    textos = {
        "pendiente": "Pendiente",
        "en_revision": "En revisión",
        "aprobada": "Aprobada",
        "rechazada": "Rechazada",
        "cerrada": "Cerrada",
    }
    return textos.get(estado_normalizado(estado), "Pendiente")


def emoji_auto(combustible=""):
    texto = (combustible or "").lower()
    if "híbrido" in texto or "hibrido" in texto:
        return "🔋"
    if "eléctrico" in texto or "electrico" in texto:
        return "⚡"
    return "🚗"


def car_image_src(vehiculo):
    imagenes = {
        "VEH001": "/assets/autos/veh001.jpg?v=18",
        "VEH002": "/assets/autos/veh002.jpg?v=18",
        "VEH003": "/assets/autos/veh003.jpg?v=18",
        "VEH004": "/assets/autos/veh004.jpg?v=18",
        "VEH005": "/assets/autos/veh005.jpg?v=18",
        "VEH006": "/assets/autos/veh006.jpg?v=18",
        "VEH007": "/assets/autos/veh007.jpg?v=18",
        "VEH008": "/assets/autos/veh008.jpg?v=18",
    }
    return imagenes.get(getattr(vehiculo, "id", ""), "/assets/autos/default.jpg?v=18")


def car_media(vehiculo):
    nombre = f"{getattr(vehiculo, 'marca', '')} {getattr(vehiculo, 'modelo', '')}".strip()
    return f'<div class="av-car-img"><img src="{car_image_src(vehiculo)}" alt="{nombre}"></div>'
