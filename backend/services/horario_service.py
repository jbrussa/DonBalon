import sqlite3
from typing import List, Optional
from classes.horario import Horario
from repositories.horario_repository import HorarioRepository


class HorarioService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = HorarioRepository(db_path, connection)

    def validate(self, obj: Horario) -> None:
        if not obj.hora_inicio:
            raise ValueError("La hora de inicio es obligatoria.")
        if not obj.hora_fin:
            raise ValueError("La hora de fin es obligatoria.")

    def insert(self, obj: Horario) -> Horario:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_horario: int) -> Optional[Horario]:
        return self.repository.get_by_id(id_horario)

    def update(self, obj: Horario) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_horario: int) -> None:
        self.repository.delete(id_horario)

    def list_all(self) -> List[Horario]:
        return self.repository.get_all()
