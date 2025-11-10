from typing import List, Optional
from classes.reserva_detalle import ReservaDetalle, from_dict as reserva_detalle_from_dict
from .base_service import BaseService


class ReservaDetalleService(BaseService):
    TABLE = "reserva_detalle"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_detalle INTEGER PRIMARY KEY,
            id_reserva INTEGER,
            id_cancha INTEGER,
            id_horario INTEGER,
            precioxhora REAL,
            costoxhora REAL,
            precio_total_item REAL
        )
        """
        self.execute(sql)

    def insert(self, obj: ReservaDetalle) -> ReservaDetalle:
        cur = self.execute(
            f"INSERT INTO {self.TABLE} (id_reserva, id_cancha, id_horario, precioxhora, costoxhora, precio_total_item) VALUES (?, ?, ?, ?, ?, ?)",
            (obj.id_reserva, obj.id_cancha, obj.id_horario, str(obj.precioxhora), str(obj.costoxhora), str(obj.precio_total_item)),
        )
        obj.id_detalle = cur.lastrowid
        return obj

    def get_by_id(self, id_detalle: int) -> Optional[ReservaDetalle]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_detalle = ?", (id_detalle,))
        if not row:
            return None
        return reserva_detalle_from_dict(dict(row))

    def update(self, obj: ReservaDetalle) -> None:
        self.execute(
            f"UPDATE {self.TABLE} SET id_reserva = ?, id_cancha = ?, id_horario = ?, precioxhora = ?, costoxhora = ?, precio_total_item = ? WHERE id_detalle = ?",
            (obj.id_reserva, obj.id_cancha, obj.id_horario, str(obj.precioxhora), str(obj.costoxhora), str(obj.precio_total_item), obj.id_detalle),
        )

    def delete(self, id_detalle: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_detalle = ?", (id_detalle,))

    def list_all(self) -> List[ReservaDetalle]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [reserva_detalle_from_dict(dict(r)) for r in rows]
