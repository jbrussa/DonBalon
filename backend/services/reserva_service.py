import sqlite3
from typing import List, Optional
from decimal import Decimal
from classes.reserva import Reserva
from repositories.reserva_repository import ReservaRepository


class ReservaService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = ReservaRepository(db_path, connection)

    def validate(self, obj: Reserva) -> None:
        if not isinstance(obj.id_cliente, int):
            raise ValueError("El id_cliente debe ser un entero.")
        if not isinstance(obj.monto_total, Decimal):
            raise ValueError("El monto_total debe ser un Decimal.")
        if not obj.fecha_reserva:
            raise ValueError("La fecha de reserva es obligatoria.")
        if not obj.estado_reserva:
            raise ValueError("El estado de la reserva es obligatorio.")
        if len(obj.estado_reserva) > 30:
            raise ValueError("El estado de la reserva no puede exceder los 30 caracteres.")

    def insert(self, obj: Reserva) -> Reserva:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_reserva: int) -> Optional[Reserva]:
        return self.repository.get_by_id(id_reserva)

    def update(self, obj: Reserva) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_reserva: int) -> None:
        self.repository.delete(id_reserva)

    def list_all(self) -> List[Reserva]:
        return self.repository.get_all()
