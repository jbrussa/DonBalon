from typing import List, Optional
from classes.estado import Estado, from_dict as estado_from_dict
from .base_service import BaseService


class EstadoService(BaseService):
    TABLE = "estado"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_estado INTEGER PRIMARY KEY,
            nombre TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Estado) -> Estado:
        cur = self.execute(f"INSERT INTO {self.TABLE} (nombre) VALUES (?)", (obj.nombre,))
        obj.id_estado = cur.lastrowid
        return obj

    def get_by_id(self, id_estado: int) -> Optional[Estado]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_estado = ?", (id_estado,))
        if not row:
            return None
        return estado_from_dict(dict(row))

    def update(self, obj: Estado) -> None:
        self.execute(f"UPDATE {self.TABLE} SET nombre = ? WHERE id_estado = ?", (obj.nombre, obj.id_estado))

    def delete(self, id_estado: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_estado = ?", (id_estado,))

    def list_all(self) -> List[Estado]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [estado_from_dict(dict(r)) for r in rows]
