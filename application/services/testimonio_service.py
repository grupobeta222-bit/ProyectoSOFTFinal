from src.domain.entities.testimonio import Testimonio
from src.domain.exceptions.domain_exception import DomainException


class TestimonioService:
    def __init__(self, testimonio_repo, cliente_repo):
        self.testimonio_repo = testimonio_repo
        self.cliente_repo = cliente_repo

    def listar(self):
        return self.testimonio_repo.find_visibles()

    def publicar(self, nombre, email, texto, foto_url="", calificacion=5):
        cliente = self.cliente_repo.find_by_email((email or "").lower().strip())
        if cliente is None:
            raise DomainException("Regístrate como cliente antes de publicar un comentario.")
        cliente.nombre = (nombre or cliente.nombre).strip()
        if foto_url:
            cliente.foto_url = foto_url.strip()
        self.cliente_repo.save_or_update(cliente)
        testimonio = Testimonio(
            cliente_id=cliente.id, nombre=cliente.nombre, email=cliente.email,
            texto=texto, calificacion=calificacion, foto_url=cliente.foto_url,
        )
        return self.testimonio_repo.save(testimonio)
