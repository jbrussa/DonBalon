import sqlite3
from typing import List, Optional
from classes.torneo import Torneo
from repositories.torneo_repository import TorneoRepository


class TorneoService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = TorneoRepository(db_path, connection)

    def validate(self, obj: Torneo) -> None:
        if not obj.nombre:
            raise ValueError("El nombre del torneo es obligatorio.")
        if len(obj.nombre) > 100:
            raise ValueError("El nombre del torneo no puede exceder los 100 caracteres.")
        if not obj.fecha_inicio:
            raise ValueError("La fecha de inicio es obligatoria.")
        if not obj.fecha_fin:
            raise ValueError("La fecha de fin es obligatoria.")

    def insert(self, obj: Torneo) -> Torneo:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_torneo: int) -> Optional[Torneo]:
        return self.repository.get_by_id(id_torneo)

    def update(self, obj: Torneo) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_torneo: int) -> None:
        self.repository.delete(id_torneo)

    def list_all(self) -> List[Torneo]:
        return self.repository.get_all()
