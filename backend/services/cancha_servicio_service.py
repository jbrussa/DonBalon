from typing import List, Optional, Tuple
from classes.cancha_servicio import CanchaServicio, from_dict as cancha_servicio_from_dict
from .base_service import BaseService


class CanchaServicioService(BaseService):
    TABLE = "cancha_servicio"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_cancha INTEGER,
            id_servicio INTEGER,
            PRIMARY KEY (id_cancha, id_servicio)
        )
        """
        self.execute(sql)

    def insert(self, obj: CanchaServicio) -> CanchaServicio:
        self.execute(f"INSERT OR REPLACE INTO {self.TABLE} (id_cancha, id_servicio) VALUES (?, ?)", (obj.id_cancha, obj.id_servicio))
        return obj

    def get_by_id(self, id_cancha: int, id_servicio: int) -> Optional[CanchaServicio]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_cancha = ? AND id_servicio = ?", (id_cancha, id_servicio))
        if not row:
            return None
        return cancha_servicio_from_dict(dict(row))

    def delete(self, id_cancha: int, id_servicio: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_cancha = ? AND id_servicio = ?", (id_cancha, id_servicio))

    def list_all(self) -> List[CanchaServicio]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [cancha_servicio_from_dict(dict(r)) for r in rows]
