from typing import List, Optional
from classes.turno import Turno, from_dict as turno_from_dict
from .base_service import BaseService


class TurnoService(BaseService):
    TABLE = "turno"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_turno INTEGER PRIMARY KEY,
            id_cancha INTEGER,
            id_horario INTEGER,
            fecha TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Turno) -> Turno:
        cur = self.execute(f"INSERT INTO {self.TABLE} (id_cancha, id_horario, fecha) VALUES (?, ?, ?)", (obj.id_cancha, obj.id_horario, obj.fecha.isoformat() if obj.fecha else None))
        obj.id_turno = cur.lastrowid
        return obj

    def get_by_id(self, id_turno: int) -> Optional[Turno]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_turno = ?", (id_turno,))
        if not row:
            return None
        return turno_from_dict(dict(row))

    def update(self, obj: Turno) -> None:
        self.execute(f"UPDATE {self.TABLE} SET id_cancha = ?, id_horario = ?, fecha = ? WHERE id_turno = ?", (obj.id_cancha, obj.id_horario, obj.fecha.isoformat() if obj.fecha else None, obj.id_turno))

    def delete(self, id_turno: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_turno = ?", (id_turno,))

    def list_all(self) -> List[Turno]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [turno_from_dict(dict(r)) for r in rows]
