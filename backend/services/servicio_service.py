from typing import List, Optional
from classes.servicio import Servicio, from_dict as servicio_from_dict
from .base_service import BaseService


class ServicioService(BaseService):
    TABLE = "servicio"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_servicio INTEGER PRIMARY KEY,
            descripcion TEXT,
            costoxservicio REAL
        )
        """
        self.execute(sql)

    def insert(self, obj: Servicio) -> Servicio:
        cur = self.execute(f"INSERT INTO {self.TABLE} (descripcion, costoxservicio) VALUES (?, ?)", (obj.descripcion, str(obj.costoxservicio)))
        obj.id_servicio = cur.lastrowid
        return obj

    def get_by_id(self, id_servicio: int) -> Optional[Servicio]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_servicio = ?", (id_servicio,))
        if not row:
            return None
        return servicio_from_dict(dict(row))

    def update(self, obj: Servicio) -> None:
        self.execute(f"UPDATE {self.TABLE} SET descripcion = ?, costoxservicio = ? WHERE id_servicio = ?", (obj.descripcion, str(obj.costoxservicio), obj.id_servicio))

    def delete(self, id_servicio: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_servicio = ?", (id_servicio,))

    def list_all(self) -> List[Servicio]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [servicio_from_dict(dict(r)) for r in rows]
