from typing import List, Optional
from classes.torneo import Torneo, from_dict as torneo_from_dict
from .base_service import BaseService


class TorneoService(BaseService):
    TABLE = "torneo"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_torneo INTEGER PRIMARY KEY,
            nombre TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Torneo) -> Torneo:
        cur = self.execute(f"INSERT INTO {self.TABLE} (nombre, fecha_inicio, fecha_fin) VALUES (?, ?, ?)", (obj.nombre, obj.fecha_inicio.isoformat() if obj.fecha_inicio else None, obj.fecha_fin.isoformat() if obj.fecha_fin else None))
        obj.id_torneo = cur.lastrowid
        return obj

    def get_by_id(self, id_torneo: int) -> Optional[Torneo]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))
        if not row:
            return None
        return torneo_from_dict(dict(row))

    def update(self, obj: Torneo) -> None:
        self.execute(f"UPDATE {self.TABLE} SET nombre = ?, fecha_inicio = ?, fecha_fin = ? WHERE id_torneo = ?", (obj.nombre, obj.fecha_inicio.isoformat() if obj.fecha_inicio else None, obj.fecha_fin.isoformat() if obj.fecha_fin else None, obj.id_torneo))

    def delete(self, id_torneo: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))

    def list_all(self) -> List[Torneo]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [torneo_from_dict(dict(r)) for r in rows]
