from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class ContactoConfig:
    whatsapp_visible: str = "+593 98 669 8212"
    whatsapp_numero: str = "593986698212"
    email: str = "grupobeta222@gmail.com"


class ContactoService:
    def __init__(self, config=None):
        self.config = config or ContactoConfig()

    def enlace_whatsapp(self):
        mensaje = quote("Hola, deseo información sobre AutoVentas Pro.")
        return f"https://wa.me/{self.config.whatsapp_numero}?text={mensaje}"

    def enlace_correo(self):
        asunto = quote("Información AutoVentas Pro")
        return f"mailto:{self.config.email}?subject={asunto}"
