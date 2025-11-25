import sqlite3
from typing import List, Optional
from datetime import date, datetime, time
from classes.turno import Turno
from repositories.turno_repository import TurnoRepository
from repositories.cancha_repository import CanchaRepository
from repositories.horario_repository import HorarioRepository


class TurnoService:
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.repository = TurnoRepository(db_path, connection)
        self.cancha_repository = CanchaRepository(db_path, connection)
        self.horario_repository = HorarioRepository(db_path, connection)

    def validate(self, obj: Turno) -> None:
        if not isinstance(obj.id_cancha, int):
            raise ValueError("El id_cancha debe ser un entero.")
        if not isinstance(obj.id_horario, int):
            raise ValueError("El id_horario debe ser un entero.")
        if not obj.fecha:
            raise ValueError("La fecha es obligatoria.")

    def insert(self, obj: Turno) -> Turno:
        self.validate(obj)
        return self.repository.create(obj)

    def get_by_id(self, id_turno: int) -> Optional[Turno]:
        return self.repository.get_by_id(id_turno)

    def update(self, obj: Turno) -> None:
        self.validate(obj)
        self.repository.update(obj)

    def delete(self, id_turno: int) -> None:
        self.repository.delete(id_turno)

    def list_all(self) -> List[Turno]:
        return self.repository.get_all()

    def crear_turnos_del_dia(self, fecha: Optional[date] = None) -> dict:
        """
        Crea todos los turnos para todas las canchas y horarios en una fecha específica.
        Si no se especifica fecha, se usa la fecha actual.
        
        Si la fecha es anterior a hoy, los turnos se crean en estado "no disponible".
        
        Args:
            fecha: Fecha para la cual crear los turnos (default: hoy)
            
        Returns:
            Diccionario con el conteo de turnos creados y omitidos
        """
        if fecha is None:
            fecha = date.today()
        
        # Verificar si la fecha es anterior a hoy
        es_fecha_pasada = fecha < date.today()
            
        # Obtener todas las canchas y horarios
        canchas = self.cancha_repository.get_all()
        horarios = self.horario_repository.get_all()
        
        creados = 0
        omitidos = 0
        
        for cancha in canchas:
            for horario in horarios:
                # Verificar si ya existe el turno
                turno_existente = self.repository.get_by_cancha_horario_fecha(
                    cancha.id_cancha, 
                    horario.id_horario, 
                    fecha
                )
                
                if turno_existente:
                    omitidos += 1
                    continue
                
                # Crear el turno
                nuevo_turno = Turno(
                    id_cancha=cancha.id_cancha,
                    id_horario=horario.id_horario,
                    fecha=fecha
                )
                
                # Si la fecha es pasada, marcar como no disponible
                if es_fecha_pasada:
                    nuevo_turno.reservar()
                
                self.repository.create(nuevo_turno)
                creados += 1
        
        return {
            "fecha": fecha.isoformat(),
            "es_fecha_pasada": es_fecha_pasada,
            "turnos_creados": creados,
            "turnos_omitidos": omitidos,
            "total_canchas": len(canchas),
            "total_horarios": len(horarios)
        }

    def expirar_turnos_pasados(self) -> dict:
        """
        Marca como 'no disponible' todos los turnos cuya fecha y hora ya pasaron.
        
        Returns:
            Diccionario con el conteo de turnos expirados
        """
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
        
        # Obtener todos los turnos
        todos_turnos = self.repository.get_all()
        expirados = 0
        
        for turno in todos_turnos:
            # Solo procesar turnos que estén disponibles
            if turno.estado_nombre.lower() != "disponible":
                continue
                
            # Obtener el horario para saber la hora de fin
            horario = self.horario_repository.get_by_id(turno.id_horario)
            if not horario:
                continue
            
            # Verificar si el turno ya pasó
            if turno.fecha < fecha_actual:
                # Fecha anterior a hoy
                turno.reservar()  # Cambia el estado a no disponible
                self.repository.update(turno)
                expirados += 1
            elif turno.fecha == fecha_actual and horario.hora_fin and horario.hora_fin <= hora_actual:
                # Mismo día pero la hora de fin ya pasó
                turno.reservar()  # Cambia el estado a no disponible
                self.repository.update(turno)
                expirados += 1
        
        return {
            "turnos_expirados": expirados,
            "fecha_hora_proceso": ahora.isoformat()
        }
