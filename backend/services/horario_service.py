import sqlite3
from typing import List, Optional
from datetime import date
from classes.horario import Horario
from repositories.horario_repository import HorarioRepository
from repositories.turno_repository import TurnoRepository


class HorarioService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = HorarioRepository(db_path, connection)
        self.turno_repository = TurnoRepository(db_path, connection)

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
        # Validar que no haya turnos futuros no disponibles (con reservas) para este horario
        turnos = self.turno_repository.get_all()
        fecha_actual = date.today()
        
        turnos_futuros_no_disponibles = [
            turno for turno in turnos
            if turno.id_horario == id_horario
            and turno.fecha and turno.fecha >= fecha_actual 
            and turno.estado_nombre.lower() in ['no disponible', 'nodisponible']
        ]
        
        if turnos_futuros_no_disponibles:
            raise ValueError(
                f"No se puede desactivar el horario porque tiene {len(turnos_futuros_no_disponibles)} "
                f"turno(s) reservado(s) para fechas futuras. Debe cancelar las reservas primero."
            )
        
        self.repository.delete(id_horario)

    def list_all(self) -> List[Horario]:
        return self.repository.get_all()
