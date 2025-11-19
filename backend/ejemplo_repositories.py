"""
Ejemplo de uso de los repositories (DAO pattern)

Este archivo muestra ejemplos de cómo usar los repositorios para realizar
operaciones CRUD en la base de datos.
"""

from repositories import (
    EstadoRepository,
    TipoCanchaRepository,
    CanchaRepository,
    ClienteRepository,
    ReservaRepository,
    TorneoRepository,
    EquipoRepository,
)
from classes.estado import Estado
from classes.tipo_cancha import TipoCancha
from classes.cancha import Cancha
from classes.cliente import Cliente
from classes.reserva import Reserva
from classes.torneo import Torneo
from classes.equipo import Equipo
from datetime import date, time
from decimal import Decimal


def ejemplo_crud_estado():
    """Ejemplo de operaciones CRUD con Estado"""
    print("\n=== EJEMPLO: CRUD de Estados ===")
    
    repo = EstadoRepository()
    
    # CREATE - Crear un nuevo estado
    nuevo_estado = Estado(nombre="Disponible")
    estado_creado = repo.create(nuevo_estado)
    print(f"✓ Estado creado: {estado_creado}")
    
    # READ - Obtener un estado por ID
    estado = repo.get_by_id(estado_creado.id_estado)
    print(f"✓ Estado obtenido: {estado}")
    
    # READ - Obtener todos los estados
    todos_estados = repo.get_all()
    print(f"✓ Total de estados: {len(todos_estados)}")
    
    # UPDATE - Actualizar un estado
    estado.nombre = "Ocupado"
    repo.update(estado)
    print(f"✓ Estado actualizado: {estado}")
    
    # DELETE - Eliminar un estado
    # repo.delete(estado.id_estado)
    # print(f"✓ Estado eliminado")
    
    repo.close()


def ejemplo_crud_cancha():
    """Ejemplo de operaciones CRUD con Cancha"""
    print("\n=== EJEMPLO: CRUD de Canchas ===")
    
    repo_cancha = CanchaRepository()
    repo_estado = EstadoRepository()
    repo_tipo = TipoCanchaRepository()
    
    # Crear estado y tipo de cancha base
    estado = Estado(nombre="Activo")
    estado_creado = repo_estado.create(estado)
    
    tipo = TipoCancha(descripcion="Cancha de futbol", precioxhora=Decimal("50.00"))
    tipo_creado = repo_tipo.create(tipo)
    
    # CREATE - Crear una cancha
    nueva_cancha = Cancha(
        id_estado=estado_creado.id_estado,
        id_tipo=tipo_creado.id_tipo,
        nombre="Cancha Central"
    )
    cancha_creada = repo_cancha.create(nueva_cancha)
    print(f"✓ Cancha creada: {cancha_creada}")
    
    # READ - Obtener una cancha
    cancha = repo_cancha.get_by_id(cancha_creada.id_cancha)
    print(f"✓ Cancha obtenida: {cancha}")
    
    # READ - Obtener canchas por tipo
    canchas_futbol = repo_cancha.get_by_tipo(tipo_creado.id_tipo)
    print(f"✓ Canchas de futbol: {len(canchas_futbol)}")
    
    # UPDATE - Actualizar cancha
    cancha.nombre = "Cancha Premium"
    repo_cancha.update(cancha)
    print(f"✓ Cancha actualizada: {cancha}")
    
    repo_cancha.close()
    repo_estado.close()
    repo_tipo.close()


def ejemplo_crud_cliente():
    """Ejemplo de operaciones CRUD con Cliente"""
    print("\n=== EJEMPLO: CRUD de Clientes ===")
    
    repo = ClienteRepository()
    
    # CREATE - Crear cliente
    nuevo_cliente = Cliente(
        nombre="Juan",
        apellido="Perez",
        dni="12345678",
        telefono="1234567890",
        mail="juan@example.com"
    )
    cliente_creado = repo.create(nuevo_cliente)
    print(f"✓ Cliente creado: {cliente_creado}")
    
    # READ - Obtener por ID
    cliente = repo.get_by_id(cliente_creado.id_cliente)
    print(f"✓ Cliente obtenido: {cliente}")
    
    # READ - Obtener por DNI
    cliente_dni = repo.get_by_dni("12345678")
    print(f"✓ Cliente por DNI: {cliente_dni}")
    
    # READ - Obtener todos
    todos = repo.get_all()
    print(f"✓ Total de clientes: {len(todos)}")
    
    # UPDATE
    cliente.mail = "juan.nuevo@example.com"
    repo.update(cliente)
    print(f"✓ Cliente actualizado: {cliente}")
    
    # VERIFICAR existencia
    existe = repo.exists(cliente.id_cliente)
    print(f"✓ Cliente existe: {existe}")
    
    repo.close()


def ejemplo_crud_torneo_y_equipos():
    """Ejemplo de operaciones CRUD con Torneos y Equipos"""
    print("\n=== EJEMPLO: CRUD de Torneos y Equipos ===")
    
    repo_torneo = TorneoRepository()
    repo_equipo = EquipoRepository()
    
    # CREATE - Crear torneo
    nuevo_torneo = Torneo(
        nombre="Campeonato 2024",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 8, 31)
    )
    torneo_creado = repo_torneo.create(nuevo_torneo)
    print(f"✓ Torneo creado: {torneo_creado}")
    
    # CREATE - Crear equipos
    equipo1 = Equipo(
        id_torneo=torneo_creado.id_torneo,
        nombre="Equipo A",
        cant_jugadores=11
    )
    equipo1_creado = repo_equipo.create(equipo1)
    print(f"✓ Equipo creado: {equipo1_creado}")
    
    # READ - Obtener equipos del torneo
    equipos_torneo = repo_equipo.get_by_torneo(torneo_creado.id_torneo)
    print(f"✓ Equipos del torneo: {len(equipos_torneo)}")
    
    # READ - Obtener torneos activos
    fecha_actual = date.today()
    torneos_activos = repo_torneo.get_activos(fecha_actual)
    print(f"✓ Torneos activos hoy: {len(torneos_activos)}")
    
    repo_torneo.close()
    repo_equipo.close()


if __name__ == "__main__":
    print("=" * 50)
    print("EJEMPLOS DE USO DE REPOSITORIES (DAO Pattern)")
    print("=" * 50)
    
    try:
        ejemplo_crud_estado()
        ejemplo_crud_cancha()
        ejemplo_crud_cliente()
        ejemplo_crud_torneo_y_equipos()
        
        print("\n" + "=" * 50)
        print("✓ TODOS LOS EJEMPLOS COMPLETADOS CORRECTAMENTE")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Error: {e}")
