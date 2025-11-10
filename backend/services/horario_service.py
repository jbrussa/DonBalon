from typing import List, Optional
from classes.horario import Horario, from_dict as horario_from_dict
from .base_service import BaseService


class HorarioService(BaseService):
    TABLE = "horario"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_horario INTEGER PRIMARY KEY,
            hora_inicio TEXT,
            hora_fin TEXT
        )
        """
        self.execute(sql)

    def insert(self, obj: Horario) -> Horario:
        cur = self.execute(f"INSERT INTO {self.TABLE} (hora_inicio, hora_fin) VALUES (?, ?)", (obj.hora_inicio.isoformat() if obj.hora_inicio else None, obj.hora_fin.isoformat() if obj.hora_fin else None))
        obj.id_horario = cur.lastrowid
        return obj

    def get_by_id(self, id_horario: int) -> Optional[Horario]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_horario = ?", (id_horario,))
        if not row:
            return None
        return horario_from_dict(dict(row))

    def update(self, obj: Horario) -> None:
        self.execute(f"UPDATE {self.TABLE} SET hora_inicio = ?, hora_fin = ? WHERE id_horario = ?", (obj.hora_inicio.isoformat() if obj.hora_inicio else None, obj.hora_fin.isoformat() if obj.hora_fin else None, obj.id_horario))

    def delete(self, id_horario: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_horario = ?", (id_horario,))

    def list_all(self) -> List[Horario]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [horario_from_dict(dict(r)) for r in rows]
