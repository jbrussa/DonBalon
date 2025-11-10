import os
import sqlite3
from typing import Any, List, Optional, Tuple


class BaseService:
    def __init__(self, db_path: Optional[str] = None):
        # Acepta opcionalmente una ruta de base de datos 
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        default_db = os.path.join(root, "database", "donbalon.db")
        self.db_path = db_path or default_db
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Conexión con base de datos
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        # Para que las filas sean accesibles como diccionarios
        self.conn.row_factory = sqlite3.Row
        # Permitir claves foraneas
        self.conn.execute("PRAGMA foreign_keys = ON")

    def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query_one(self, sql: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def query_all(self, sql: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass
