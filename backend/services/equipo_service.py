from typing import List, Optional
from classes.equipo import Equipo, from_dict as equipo_from_dict
from .base_service import BaseService


class EquipoService(BaseService):
    TABLE = "equipo"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_equipo INTEGER PRIMARY KEY,
            id_torneo INTEGER,
            nombre TEXT,
            cant_jugadores INTEGER,
            FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
        )
        """
        self.execute(sql)

    def insert(self, obj: Equipo) -> Equipo:
        cur = self.execute(f"INSERT INTO {self.TABLE} (id_torneo, nombre, cant_jugadores) VALUES (?, ?, ?)", (obj.id_torneo, obj.nombre, obj.cant_jugadores))
        obj.id_equipo = cur.lastrowid
        return obj

    def get_by_id(self, id_equipo: int) -> Optional[Equipo]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_equipo = ?", (id_equipo,))
        if not row:
            return None
        return equipo_from_dict(dict(row))

    def update(self, obj: Equipo) -> None:
        self.execute(f"UPDATE {self.TABLE} SET id_torneo = ?, nombre = ?, cant_jugadores = ? WHERE id_equipo = ?", (obj.id_torneo, obj.nombre, obj.cant_jugadores, obj.id_equipo))

    def delete(self, id_equipo: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_equipo = ?", (id_equipo,))

    def list_all(self) -> List[Equipo]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [equipo_from_dict(dict(r)) for r in rows]

    def get_by_torneo(self, id_torneo: int) -> List[Equipo]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE} WHERE id_torneo = ?", (id_torneo,))
        return [equipo_from_dict(dict(r)) for r in rows]
