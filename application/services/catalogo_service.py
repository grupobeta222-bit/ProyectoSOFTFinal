class CatalogoService:

    def __init__(self, vehiculo_repo, plan_repo):
        self.vehiculo_repo = vehiculo_repo
        self.plan_repo     = plan_repo

    def listar_vehiculos(self):
        return self.vehiculo_repo.find_all()

    def listar_planes(self):
        return self.plan_repo.find_all()
