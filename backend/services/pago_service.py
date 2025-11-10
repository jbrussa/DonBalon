from typing import List, Optional
from classes.pago import Pago, from_dict as pago_from_dict
from .base_service import BaseService


class PagoService(BaseService):
    TABLE = "pago"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_pago INTEGER PRIMARY KEY,
            id_reserva INTEGER,
            id_metodo_pago INTEGER,
            fecha_pago TEXT,
            monto REAL,
            estado_pago TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Pago) -> Pago:
        cur = self.execute(
            f"INSERT INTO {self.TABLE} (id_reserva, id_metodo_pago, fecha_pago, monto, estado_pago) VALUES (?, ?, ?, ?, ?)",
            (obj.id_reserva, obj.id_metodo_pago, obj.fecha_pago.isoformat() if obj.fecha_pago else None, str(obj.monto), obj.estado_pago),
        )
        obj.id_pago = cur.lastrowid
        return obj

    def get_by_id(self, id_pago: int) -> Optional[Pago]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_pago = ?", (id_pago,))
        if not row:
            return None
        return pago_from_dict(dict(row))

    def update(self, obj: Pago) -> None:
        self.execute(
            f"UPDATE {self.TABLE} SET id_reserva = ?, id_metodo_pago = ?, fecha_pago = ?, monto = ?, estado_pago = ? WHERE id_pago = ?",
            (obj.id_reserva, obj.id_metodo_pago, obj.fecha_pago.isoformat() if obj.fecha_pago else None, str(obj.monto), obj.estado_pago, obj.id_pago),
        )

    def delete(self, id_pago: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_pago = ?", (id_pago,))

    def list_all(self) -> List[Pago]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [pago_from_dict(dict(r)) for r in rows]
