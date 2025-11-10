from typing import List, Optional
from classes.tipo_pago import TipoPago, from_dict as tipo_pago_from_dict
from .base_service import BaseService


class TipoPagoService(BaseService):
    TABLE = "tipo_pago"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_tipo_pago INTEGER PRIMARY KEY,
            descripcion TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: TipoPago) -> TipoPago:
        cur = self.execute(f"INSERT INTO {self.TABLE} (descripcion) VALUES (?)", (obj.descripcion,))
        obj.id_tipo_pago = cur.lastrowid
        return obj

    def get_by_id(self, id_tipo_pago: int) -> Optional[TipoPago]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_tipo_pago = ?", (id_tipo_pago,))
        if not row:
            return None
        return tipo_pago_from_dict(dict(row))

    def update(self, obj: TipoPago) -> None:
        self.execute(f"UPDATE {self.TABLE} SET descripcion = ? WHERE id_tipo_pago = ?", (obj.descripcion, obj.id_tipo_pago))

    def delete(self, id_tipo_pago: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_tipo_pago = ?", (id_tipo_pago,))

    def list_all(self) -> List[TipoPago]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [tipo_pago_from_dict(dict(r)) for r in rows]
