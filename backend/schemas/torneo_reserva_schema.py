from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import date


class EquipoInput(BaseModel):
    """Datos de un equipo para el torneo"""
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del equipo")
    cant_jugadores: int = Field(..., ge=5, description="Cantidad de jugadores (mínimo 5)")


class TorneoReservaRequest(BaseModel):
    """Request para crear un torneo con su reserva"""
    id_cliente: int = Field(..., description="ID del cliente que reserva")
    nombre_torneo: str = Field(..., min_length=1, max_length=100, description="Nombre del torneo")
    fecha_inicio: date = Field(..., description="Fecha de inicio del torneo")
    fecha_fin: date = Field(..., description="Fecha de fin del torneo")
    equipos: List[EquipoInput] = Field(..., min_items=2, description="Lista de equipos (mínimo 2)")
    total_partidos: int = Field(..., ge=1, description="Cantidad total de partidos del torneo")
    partidos_por_dia: int = Field(..., ge=1, description="Cantidad de partidos a jugar por día")
    id_metodo_pago: int = Field(..., description="ID del método de pago")
    tipos_cancha: List[int] = Field(..., min_items=1, description="IDs de tipos de cancha permitidos (mínimo 1)")
    
    @field_validator('equipos')
    @classmethod
    def validate_equipos_nombres_unicos(cls, v):
        """Validar que no haya nombres de equipos duplicados en el mismo torneo"""
        nombres = [equipo.nombre.lower().strip() for equipo in v]
        if len(nombres) != len(set(nombres)):
            raise ValueError('No puede haber dos equipos con el mismo nombre en el mismo torneo')
        return v
    
    @field_validator('fecha_fin')
    @classmethod
    def validate_fechas(cls, v, info):
        """Validar que fecha_fin >= fecha_inicio"""
        if 'fecha_inicio' in info.data and v < info.data['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser mayor o igual a la fecha de inicio')
        return v
    
    @field_validator('fecha_inicio')
    @classmethod
    def validate_fecha_inicio(cls, v):
        """Validar que fecha_inicio >= fecha actual"""
        from datetime import date as dt_date
        if v < dt_date.today():
            raise ValueError('La fecha de inicio no puede ser anterior a la fecha actual')
        return v


class TurnoSeleccionado(BaseModel):
    """Información de un turno seleccionado automáticamente"""
    id_cancha: int
    nombre_cancha: str
    id_horario: int
    hora_inicio: str
    fecha: date
    precio: str


class TorneoReservaResponse(BaseModel):
    """Response con el torneo creado y los turnos seleccionados"""
    id_torneo: int
    nombre_torneo: str
    fecha_inicio: date
    fecha_fin: date
    equipos: List[dict]
    turnos_seleccionados: List[TurnoSeleccionado]
    total_partidos: int
    partidos_por_dia: int
    max_partidos_por_dia: int
    monto_total: str
    dias_necesarios: int
