import sqlite3
from typing import List, Optional
from decimal import Decimal
from classes.reserva_detalle import ReservaDetalle
from repositories.reserva_detalle_repository import ReservaDetalleRepository


class ReservaDetalleService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = ReservaDetalleRepository(db_path, connection)

    def validate(self, obj: ReservaDetalle) -> None:
        if not isinstance(obj.id_reserva, int):
            raise ValueError("El id_reserva debe ser un entero.")
        if not isinstance(obj.id_turno, int):
            raise ValueError("El id_turno debe ser un entero.")
        if not isinstance(obj.precio_total_item, Decimal):
            raise ValueError("El precio_total_item debe ser un Decimal.")

    def insert(self, obj: ReservaDetalle) -> ReservaDetalle:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_detalle: int) -> Optional[ReservaDetalle]:
        return self.repository.get_by_id(id_detalle)

    def update(self, obj: ReservaDetalle) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_detalle: int) -> None:
        self.repository.delete(id_detalle)

    def list_all(self) -> List[ReservaDetalle]:
        return self.repository.get_all()
