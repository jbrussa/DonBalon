from typing import List, Optional
from classes.tipo_cancha import TipoCancha, from_dict as tipo_cancha_from_dict
from .base_service import BaseService


class TipoCanchaService(BaseService):
    TABLE = "tipo_cancha"

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path)
        self.create_table()

    def create_table(self):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            id_tipo INTEGER PRIMARY KEY,
            descripcion TEXT,
            precioxhora REAL
        )
        """
        self.execute(sql)

    def insert(self, obj: TipoCancha) -> TipoCancha:
        cur = self.execute(f"INSERT INTO {self.TABLE} (descripcion, precioxhora) VALUES (?, ?)", (obj.descripcion, str(obj.precioxhora)))
        obj.id_tipo = cur.lastrowid
        return obj

    def get_by_id(self, id_tipo: int) -> Optional[TipoCancha]:
        row = self.query_one(f"SELECT * FROM {self.TABLE} WHERE id_tipo = ?", (id_tipo,))
        if not row:
            return None
        return tipo_cancha_from_dict(dict(row))

    def update(self, obj: TipoCancha) -> None:
        self.execute(f"UPDATE {self.TABLE} SET descripcion = ?, precioxhora = ? WHERE id_tipo = ?", (obj.descripcion, str(obj.precioxhora), obj.id_tipo))

    def delete(self, id_tipo: int) -> None:
        self.execute(f"DELETE FROM {self.TABLE} WHERE id_tipo = ?", (id_tipo,))

    def list_all(self) -> List[TipoCancha]:
        rows = self.query_all(f"SELECT * FROM {self.TABLE}")
        return [tipo_cancha_from_dict(dict(r)) for r in rows]
