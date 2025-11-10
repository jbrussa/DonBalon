from typing import List, Optional
from classes.reserva import Reserva, from_dict as reserva_from_dict
from .base_service import BaseService


class ReservaService(BaseService):
    TABLE = "reserva"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_reserva INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            id_horario INTEGER,
            monto_total REAL,
            fecha_reserva TEXT,
            estado_reserva TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Reserva) -> Reserva:
        cur = self.execute(
            f"INSERT INTO {self.TABLE} (id_cliente, id_horario, monto_total, fecha_reserva, estado_reserva) VALUES (?, ?, ?, ?, ?)",
            (obj.id_cliente, obj.id_horario, str(obj.monto_total), obj.fecha_reserva.isoformat() if obj.fecha_reserva else None, obj.estado_reserva),
        )
        obj.id_reserva = cur.lastrowid
        return obj

    def get_by_id(self, id_reserva: int) -> Optional[Reserva]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))
        if not row:
            return None
        return reserva_from_dict(dict(row))

    def update(self, obj: Reserva) -> None:
        self.execute(
            f"UPDATE {self.TABLE} SET id_cliente = ?, id_horario = ?, monto_total = ?, fecha_reserva = ?, estado_reserva = ? WHERE id_reserva = ?",
            (obj.id_cliente, obj.id_horario, str(obj.monto_total), obj.fecha_reserva.isoformat() if obj.fecha_reserva else None, obj.estado_reserva, obj.id_reserva),
        )

    def delete(self, id_reserva: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_reserva = ?", (id_reserva,))

    def list_all(self) -> List[Reserva]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [reserva_from_dict(dict(r)) for r in rows]
