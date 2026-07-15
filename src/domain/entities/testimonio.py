from src.domain.exceptions.domain_exception import DomainException


class Testimonio:
    def __init__(self, cliente_id, nombre, email, texto, calificacion=5,
                 id=None, foto_url="", fecha=None, visible=True):
        texto = (texto or "").strip()
        if not cliente_id or len(texto) < 10:
            raise DomainException("El comentario debe tener al menos 10 caracteres.")
        calificacion = int(calificacion)
        if calificacion < 1 or calificacion > 5:
            raise DomainException("La calificacion debe estar entre 1 y 5.")
        self.id = id
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.email = email
        self.texto = texto
        self.calificacion = calificacion
        self.foto_url = foto_url
        self.fecha = fecha
        self.visible = bool(visible)

    @property
    def iniciales(self):
        partes = (self.nombre or "Cliente").strip().split()
        return "".join(parte[0].upper() for parte in partes[:2]) or "CL"
