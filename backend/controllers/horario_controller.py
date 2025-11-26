from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.horario_schema import HorarioCreate, HorarioUpdate, HorarioResponse
from services.horario_service import HorarioService
from classes.horario import Horario
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/horarios", tags=["Horarios"])


def get_horario_service():
    """Dependency para obtener instancia de HorarioService"""
    db_conn = DatabaseConnection()
    return HorarioService(connection=db_conn.get_connection())


@router.get("/", response_model=List[HorarioResponse])
def list_horarios(service: HorarioService = Depends(get_horario_service)):
    """Listar todos los horarios"""
    horarios = service.list_all()
    return [HorarioResponse(**horario.to_dict()) for horario in horarios]


@router.get("/{id_horario}", response_model=HorarioResponse)
def get_horario(id_horario: int, service: HorarioService = Depends(get_horario_service)):
    """Obtener un horario por ID"""
    horario = service.get_by_id(id_horario)
    if not horario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horario con ID {id_horario} no encontrado"
        )
    return HorarioResponse(**horario.to_dict())


@router.post("/", response_model=HorarioResponse, status_code=status.HTTP_201_CREATED)
def create_horario(horario_data: HorarioCreate, service: HorarioService = Depends(get_horario_service)):
    """Crear un nuevo horario"""
    # Conversión manual de Schema a Clase de Dominio
    horario = Horario(
        hora_inicio=horario_data.hora_inicio,
        hora_fin=horario_data.hora_fin
    )
    
    try:
        created_horario = service.insert(horario)
        return HorarioResponse(**created_horario.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_horario}", response_model=HorarioResponse)
def update_horario(id_horario: int, horario_data: HorarioUpdate, service: HorarioService = Depends(get_horario_service)):
    """Actualizar un horario existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    horario_actual = service.get_by_id(id_horario)
    if not horario_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horario con ID {id_horario} no encontrado"
        )
    
    # 2. Merge inteligente
    nueva_hora_inicio = horario_data.hora_inicio if horario_data.hora_inicio is not None else horario_actual.hora_inicio
    nueva_hora_fin = horario_data.hora_fin if horario_data.hora_fin is not None else horario_actual.hora_fin

    # 3. Crear la instancia para actualizar con los datos mezclados
    horario_a_guardar = Horario(
        id_horario=id_horario,
        hora_inicio=nueva_hora_inicio,
        hora_fin=nueva_hora_fin
    )
    
    try:
        service.update(horario_a_guardar)
        return HorarioResponse(**horario_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_horario(id_horario: int, service: HorarioService = Depends(get_horario_service)):
    """Eliminar un horario"""
    existing = service.get_by_id(id_horario)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horario con ID {id_horario} no encontrado"
        )
    
    try:
        service.delete(id_horario)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
