from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.torneo_schema import TorneoCreate, TorneoUpdate, TorneoResponse
from schemas.torneo_reserva_schema import TorneoReservaRequest, TorneoReservaResponse
from services.torneo_service import TorneoService
from services.torneo_reserva_service import TorneoReservaService
from classes.torneo import Torneo
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/torneos", tags=["Torneos"])


def get_torneo_service():
    """Dependency para obtener instancia de TorneoService"""
    db_conn = DatabaseConnection()
    return TorneoService(connection=db_conn.get_connection())


def get_torneo_reserva_service():
    """Dependency para obtener instancia de TorneoReservaService"""
    db_conn = DatabaseConnection()
    return TorneoReservaService(connection=db_conn.get_connection())


@router.get("/", response_model=List[TorneoResponse])
def list_torneos(service: TorneoService = Depends(get_torneo_service)):
    """Listar todos los torneos"""
    torneos = service.list_all()
    return [TorneoResponse(**torneo.to_dict()) for torneo in torneos]


@router.get("/max-partidos-dia", response_model=dict)
def get_max_partidos_dia(
    num_equipos: int = None,
    tipos_cancha: str = None,
    service: TorneoReservaService = Depends(get_torneo_reserva_service)
):
    """Obtener el máximo de partidos que se pueden jugar por día
    
    tipos_cancha: string con IDs separados por comas, ej: "1,2,3"
    """
    tipos_list = None
    if tipos_cancha:
        try:
            tipos_list = [int(x.strip()) for x in tipos_cancha.split(',') if x.strip()]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tipos_cancha debe ser una lista de números separados por comas"
            )
    
    max_partidos = service.calcular_max_partidos_por_dia(num_equipos, tipos_list)
    return {
        "max_partidos_por_dia": max_partidos,
        "mensaje": f"Se pueden jugar máximo {max_partidos} partidos por día"
    }


@router.get("/validar-disponibilidad", response_model=dict)
def validar_disponibilidad(
    fecha_inicio: str,
    fecha_fin: str,
    total_partidos: int,
    partidos_por_dia: int,
    num_equipos: int,
    tipos_cancha: str = None,
    service: TorneoReservaService = Depends(get_torneo_reserva_service)
):
    """Validar si hay suficientes turnos disponibles para un torneo
    
    fecha_inicio: formato YYYY-MM-DD
    fecha_fin: formato YYYY-MM-DD
    num_equipos: cantidad de equipos en el torneo
    tipos_cancha: string con IDs separados por comas, ej: "1,2,3"
    """
    from datetime import datetime
    
    try:
        fecha_inicio_date = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_date = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las fechas deben tener el formato YYYY-MM-DD"
        )
    
    tipos_list = None
    if tipos_cancha:
        try:
            tipos_list = [int(x.strip()) for x in tipos_cancha.split(',') if x.strip()]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tipos_cancha debe ser una lista de números separados por comas"
            )
    
    resultado = service.validar_disponibilidad_turnos(
        fecha_inicio_date,
        fecha_fin_date,
        total_partidos,
        partidos_por_dia,
        num_equipos,
        tipos_list
    )
    
    return resultado


@router.get("/{id_torneo}", response_model=TorneoResponse)
def get_torneo(id_torneo: int, service: TorneoService = Depends(get_torneo_service)):
    """Obtener un torneo por ID"""
    torneo = service.get_by_id(id_torneo)
    if not torneo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    return TorneoResponse(**torneo.to_dict())


@router.post("/", response_model=TorneoResponse, status_code=status.HTTP_201_CREATED)
def create_torneo(torneo_data: TorneoCreate, service: TorneoService = Depends(get_torneo_service)):
    """Crear un nuevo torneo"""
    # Conversión manual de Schema a Clase de Dominio
    torneo = Torneo(
        nombre=torneo_data.nombre,
        fecha_inicio=torneo_data.fecha_inicio,
        fecha_fin=torneo_data.fecha_fin
    )
    
    try:
        created_torneo = service.insert(torneo)
        return TorneoResponse(**created_torneo.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_torneo}", response_model=TorneoResponse)
def update_torneo(id_torneo: int, torneo_data: TorneoUpdate, service: TorneoService = Depends(get_torneo_service)):
    """Actualizar un torneo existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    torneo_actual = service.get_by_id(id_torneo)
    if not torneo_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    
    # 2. Merge inteligente
    nuevo_nombre = torneo_data.nombre if torneo_data.nombre is not None else torneo_actual.nombre
    nueva_fecha_inicio = torneo_data.fecha_inicio if torneo_data.fecha_inicio is not None else torneo_actual.fecha_inicio
    nueva_fecha_fin = torneo_data.fecha_fin if torneo_data.fecha_fin is not None else torneo_actual.fecha_fin

    # 3. Crear la instancia para actualizar con los datos mezclados
    torneo_a_guardar = Torneo(
        id_torneo=id_torneo,
        nombre=nuevo_nombre,
        fecha_inicio=nueva_fecha_inicio,
        fecha_fin=nueva_fecha_fin
    )
    
    try:
        service.update(torneo_a_guardar)
        return TorneoResponse(**torneo_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_torneo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_torneo(id_torneo: int, service: TorneoService = Depends(get_torneo_service)):
    """Eliminar un torneo"""
    existing = service.get_by_id(id_torneo)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Torneo con ID {id_torneo} no encontrado"
        )
    
    service.delete(id_torneo)
    return None


@router.post("/reservar", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_torneo_con_reserva(
    data: TorneoReservaRequest,
    service: TorneoReservaService = Depends(get_torneo_reserva_service)
):
    """
    Crear un torneo completo con reserva automática de turnos.
    
    El sistema:
    1. Crea el torneo y los equipos
    2. Calcula el total de partidos (todos contra todos)
    3. Selecciona automáticamente los turnos priorizando simultaneidad
    4. Crea la reserva y marca los turnos como no disponibles
    5. Registra el pago
    """
    try:
        resultado = service.crear_torneo_con_reserva(data)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el torneo: {str(e)}"
        )
