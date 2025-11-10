from typing import List, Optional
from classes.metodo_pago import MetodoPago, from_dict as metodo_pago_from_dict
from .base_service import BaseService


class MetodoPagoService(BaseService):
    TABLE = "metodo_pago"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_metodo_pago INTEGER PRIMARY KEY,
            descripcion TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: MetodoPago) -> MetodoPago:
        cur = self.execute(f"INSERT INTO {self.TABLE} (descripcion) VALUES (?)", (obj.descripcion,))
        obj.id_metodo_pago = cur.lastrowid
        return obj

    def get_by_id(self, id_metodo_pago: int) -> Optional[MetodoPago]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_metodo_pago = ?", (id_metodo_pago,))
        if not row:
            return None
        return metodo_pago_from_dict(dict(row))

    def update(self, obj: MetodoPago) -> None:
        self.execute(f"UPDATE {self.TABLE} SET descripcion = ? WHERE id_metodo_pago = ?", (obj.descripcion, obj.id_metodo_pago))

    def delete(self, id_metodo_pago: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_metodo_pago = ?", (id_metodo_pago,))

    def list_all(self) -> List[MetodoPago]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [metodo_pago_from_dict(dict(r)) for r in rows]
