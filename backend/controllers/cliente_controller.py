from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from services.cliente_service import ClienteService
from classes.cliente import Cliente
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_cliente_service():
    """Dependency para obtener instancia de ClienteService"""
    db_conn = DatabaseConnection()
    return ClienteService(connection=db_conn.get_connection())


@router.get("/", response_model=List[ClienteResponse])
def list_clientes(service: ClienteService = Depends(get_cliente_service)):
    """Listar todos los clientes"""
    clientes = service.list_all()
    return [ClienteResponse(**cliente.to_dict()) for cliente in clientes]


@router.get("/{id_cliente}", response_model=ClienteResponse)
def get_cliente(id_cliente: int, service: ClienteService = Depends(get_cliente_service)):
    """Obtener un cliente por ID"""
    cliente = service.get_by_id(id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {id_cliente} no encontrado"
        )
    return ClienteResponse(**cliente.to_dict())


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente_data: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    """Crear un nuevo cliente"""
    # Conversión manual de Schema a Clase de Dominio
    cliente = Cliente(
        nombre=cliente_data.nombre,
        apellido=cliente_data.apellido,
        mail=cliente_data.mail,
        telefono=cliente_data.telefono,
        password=cliente_data.password,
        admin=cliente_data.admin
    )
    
    try:
        created_cliente = service.insert(cliente)
        return ClienteResponse(**created_cliente.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_cliente}", response_model=ClienteResponse)
def update_cliente(id_cliente: int, cliente_data: ClienteUpdate, service: ClienteService = Depends(get_cliente_service)):
    """Actualizar un cliente existente (Maneja parciales correctamente)"""
    # 1. Verificar y obtener datos ACTUALES de la BD
    cliente_actual = service.get_by_id(id_cliente)
    if not cliente_actual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {id_cliente} no encontrado"
        )
    
    # 2. Merge inteligente
    nuevo_nombre = cliente_data.nombre if cliente_data.nombre is not None else cliente_actual.nombre
    nuevo_apellido = cliente_data.apellido if cliente_data.apellido is not None else cliente_actual.apellido
    nuevo_mail = cliente_data.mail if cliente_data.mail is not None else cliente_actual.mail
    nuevo_telefono = cliente_data.telefono if cliente_data.telefono is not None else cliente_actual.telefono
    nuevo_password = cliente_data.password if cliente_data.password is not None else cliente_actual.password
    nuevo_admin = cliente_data.admin if cliente_data.admin is not None else cliente_actual.admin

    # 3. Crear la instancia para actualizar con los datos mezclados
    cliente_a_guardar = Cliente(
        id_cliente=id_cliente,
        nombre=nuevo_nombre,
        apellido=nuevo_apellido,
        mail=nuevo_mail,
        telefono=nuevo_telefono,
        password=nuevo_password,
        admin=nuevo_admin
    )
    
    try:
        service.update(cliente_a_guardar)
        return ClienteResponse(**cliente_a_guardar.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(id_cliente: int, service: ClienteService = Depends(get_cliente_service)):
    """Eliminar un cliente"""
    existing = service.get_by_id(id_cliente)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {id_cliente} no encontrado"
        )
    
    service.delete(id_cliente)
    return None
