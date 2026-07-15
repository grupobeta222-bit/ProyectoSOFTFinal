from src.infrastructure.security import verify_password


class AuthService:
    def __init__(self, usuario_repo):
        self.usuario_repo = usuario_repo

    def autenticar(self, email, password):
        resultado = self.usuario_repo.find_by_email((email or "").lower().strip())
        if resultado is None:
            return None
        usuario, password_hash = resultado
        if not usuario.activo or not verify_password(password, password_hash):
            return None
        return usuario.datos_sesion()

    def listar_asesores(self):
        return [usuario.datos_sesion() | {
            "id": usuario.id,
            "usuario": usuario.email,
            "nombre": usuario.nombre,
            "especialidad": usuario.especialidad,
            "rating": usuario.rating,
        } for usuario in self.usuario_repo.find_asesores()]
