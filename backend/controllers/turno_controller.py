from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import date
from schemas.turno_schema import TurnoCreate, TurnoUpdate, TurnoResponse
from services.turno_service import TurnoService
from classes.turno import Turno
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/turnos", tags=["Turnos"])


def get_turno_service():
    """Dependency para obtener instancia de TurnoService"""
    db_conn = DatabaseConnection()
    return TurnoService(connection=db_conn.get_connection())

@router.get("", response_model=List[TurnoResponse])
@router.get("/", response_model=List[TurnoResponse])
def list_turnos(service: TurnoService = Depends(get_turno_service)):
    """Listar todos los turnos"""
    turnos = service.list_all()
    return [TurnoResponse(**turno.to_dict()) for turno in turnos]


@router.get("/{id_turno}", response_model=TurnoResponse)
def get_turno(id_turno: int, service: TurnoService = Depends(get_turno_service)):
    """Obtener un turno por ID"""
    turno = service.get_by_id(id_turno)
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno con ID {id_turno} no encontrado"
        )
    return TurnoResponse(**turno.to_dict())


@router.post("/", response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
def create_turno(turno_data: TurnoCreate, service: TurnoService = Depends(get_turno_service)):
    """Crear un nuevo turno"""
    # Conversión manual de Schema a Clase de Dominio
    turno = Turno(
        id_cancha=turno_data.id_cancha,
        id_horario=turno_data.id_horario,
        fecha=turno_data.fecha
    )
    
    try:
        created_turno = service.insert(turno)
        return TurnoResponse(**created_turno.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_turno}", response_model=TurnoResponse)
def update_turno(id_turno: int, turno_data: TurnoUpdate, service: TurnoService = Depends(get_turno_service)):
    """Actualizar un turno existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    turno_actual = service.get_by_id(id_turno)
    if not turno_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno con ID {id_turno} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_cancha = turno_data.id_cancha if turno_data.id_cancha is not None else turno_actual.id_cancha
    nuevo_horario = turno_data.id_horario if turno_data.id_horario is not None else turno_actual.id_horario
    nueva_fecha = turno_data.fecha if turno_data.fecha is not None else turno_actual.fecha

    # 3. Crear la instancia para actualizar con los datos mezclados
    turno_a_guardar = Turno(
        id_turno=id_turno,
        id_cancha=nueva_cancha,
        id_horario=nuevo_horario,
        fecha=nueva_fecha
    )
    
    try:
        service.update(turno_a_guardar)
        return TurnoResponse(**turno_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_turno}", status_code=status.HTTP_204_NO_CONTENT)
def delete_turno(id_turno: int, service: TurnoService = Depends(get_turno_service)):
    """Eliminar un turno"""
    existing = service.get_by_id(id_turno)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno con ID {id_turno} no encontrado"
        )
    
    service.delete(id_turno)
    return None


@router.post("/crear-del-dia", status_code=status.HTTP_200_OK)
def crear_turnos_del_dia(fecha: Optional[date] = None, service: TurnoService = Depends(get_turno_service)):
    """
    Crea todos los turnos para todas las canchas y horarios en una fecha específica.
    Si no se especifica fecha, se usa la fecha actual.
    """
    try:
        resultado = service.crear_turnos_del_dia(fecha)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear turnos: {str(e)}"
        )


@router.post("/expirar-pasados", status_code=status.HTTP_200_OK)
def expirar_turnos_pasados(service: TurnoService = Depends(get_turno_service)):
    """
    Marca como 'no disponible' todos los turnos cuya fecha y hora ya pasaron.
    """
    try:
        resultado = service.expirar_turnos_pasados()
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al expirar turnos: {str(e)}"
        )
