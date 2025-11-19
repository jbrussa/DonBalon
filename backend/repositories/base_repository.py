"""
Base Repository - Clase base para todos los repositorios DAO (Data Access Object)
Proporciona métodos genéricos para operaciones CRUD
"""

import os
import sqlite3
from typing import Any, List, Optional, Tuple


class BaseRepository:
    """Clase base que proporciona métodos comunes para acceso a datos"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa la conexión a la base de datos SQLite

        Args:
            db_path: Ruta a la base de datos. Si es None, se busca en la carpeta backend
        """
        if db_path is None:
            # Obtener la ruta al archivo donbalon.db en la carpeta backend
            root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            db_path = os.path.join(root, "donbalon.db")

        self.db_path = db_path

        # Crear conexión a la base de datos
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        # Permitir acceso a las filas como diccionarios
        self.conn.row_factory = sqlite3.Row
        # Habilitar restricciones de claves foráneas
        self.conn.execute("PRAGMA foreign_keys = ON")

    def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """
        Ejecuta una sentencia SQL (INSERT, UPDATE, DELETE)

        Args:
            sql: Sentencia SQL a ejecutar
            params: Parámetros para la sentencia

        Returns:
            Cursor con el resultado de la ejecución
        """
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query_one(self, sql: str, params: Tuple[Any, ...] = ()) -> Optional[sqlite3.Row]:
        """
        Ejecuta una sentencia SQL SELECT y retorna una fila

        Args:
            sql: Sentencia SQL a ejecutar
            params: Parámetros para la sentencia

        Returns:
            Una fila (Row) o None si no hay resultados
        """
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def query_all(self, sql: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        """
        Ejecuta una sentencia SQL SELECT y retorna todas las filas

        Args:
            sql: Sentencia SQL a ejecutar
            params: Parámetros para la sentencia

        Returns:
            Lista de filas (Row objects)
        """
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        """Cierra la conexión a la base de datos"""
        try:
            self.conn.close()
        except Exception:
            pass

    def __del__(self):
        """Asegura que la conexión se cierre al destruir el objeto"""
        self.close()
