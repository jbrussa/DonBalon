from typing import List, Optional
from classes.cancha import Cancha, from_dict as cancha_from_dict
from .base_service import BaseService


class CanchaService(BaseService):
    TABLE = "cancha"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_cancha INTEGER PRIMARY KEY,
            id_estado INTEGER,
            id_tipo INTEGER,
            nombre TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Cancha) -> Cancha:
        cur = self.execute(f"INSERT INTO {self.TABLE} (id_estado, id_tipo, nombre) VALUES (?, ?, ?)", (obj.id_estado, obj.id_tipo, obj.nombre))
        obj.id_cancha = cur.lastrowid
        return obj

    def get_by_id(self, id_cancha: int) -> Optional[Cancha]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))
        if not row:
            return None
        return cancha_from_dict(dict(row))

    def update(self, obj: Cancha) -> None:
        self.execute(f"UPDATE {self.TABLE} SET id_estado = ?, id_tipo = ?, nombre = ? WHERE id_cancha = ?", (obj.id_estado, obj.id_tipo, obj.nombre, obj.id_cancha))

    def delete(self, id_cancha: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_cancha = ?", (id_cancha,))

    def list_all(self) -> List[Cancha]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [cancha_from_dict(dict(r)) for r in rows]
