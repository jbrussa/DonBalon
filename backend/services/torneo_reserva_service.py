"""
TorneoReservaService - Servicio para gestionar torneos y sus reservas
Incluye lógica de selección automática de turnos consecutivos/simultáneos
"""

import sqlite3
from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import date, timedelta
from classes.torneo import Torneo
from classes.equipo import Equipo
from classes.reserva import Reserva
from classes.reserva_detalle import ReservaDetalle
from classes.turno import Turno
from classes.pago import Pago
from repositories.torneo_repository import TorneoRepository
from repositories.equipo_repository import EquipoRepository
from repositories.reserva_repository import ReservaRepository
from repositories.reserva_detalle_repository import ReservaDetalleRepository
from repositories.turno_repository import TurnoRepository
from repositories.pago_repository import PagoRepository
from repositories.cancha_repository import CanchaRepository
from repositories.horario_repository import HorarioRepository
from repositories.tipo_cancha_repository import TipoCanchaRepository
from repositories.cancha_servicio_repository import CanchaServicioRepository
from repositories.servicio_repository import ServicioRepository
from repositories.metodo_pago_repository import MetodoPagoRepository
from schemas.torneo_reserva_schema import TorneoReservaRequest, EquipoInput
from data.database_connection import DatabaseConnection

from classes.estado_reserva.reserva_pagada import ReservaPagada
from classes.estado_reserva.reserva_pendiente import ReservaPendiente
from classes.estado_turno.turno_no_disponible import TurnoNoDisponible
from classes.estado_turno.turno_disponible import TurnoDisponible


class TorneoReservaService:
    """Servicio para manejar la creación de torneos con reserva automática de turnos"""
    
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.db_conn = DatabaseConnection()
        self.connection = connection if connection else self.db_conn.get_connection()
        
        # Repositorios
        self.torneo_repo = TorneoRepository(connection=self.connection)
        self.equipo_repo = EquipoRepository(connection=self.connection)
        self.reserva_repo = ReservaRepository(connection=self.connection)
        self.detalle_repo = ReservaDetalleRepository(connection=self.connection)
        self.turno_repo = TurnoRepository(connection=self.connection)
        self.pago_repo = PagoRepository(connection=self.connection)
        self.cancha_repo = CanchaRepository(connection=self.connection)
        self.horario_repo = HorarioRepository(connection=self.connection)
        self.tipo_cancha_repo = TipoCanchaRepository(connection=self.connection)
        self.cancha_servicio_repo = CanchaServicioRepository(connection=self.connection)
        self.servicio_repo = ServicioRepository(connection=self.connection)
        self.metodo_pago_repo = MetodoPagoRepository(connection=self.connection)
    
    def calcular_max_partidos_por_dia(self, num_equipos: int = None, tipos_cancha: List[int] = None) -> int:
        """
        Calcula el máximo de partidos que se pueden jugar por día
        basado en la cantidad de canchas, horarios y equipos disponibles
        
        Si se proporciona num_equipos, considera que el máximo de partidos
        simultáneos es num_equipos // 2 (cada partido requiere 2 equipos)
        
        Si se proporcionan tipos_cancha, solo cuenta canchas de esos tipos
        """
        canchas = self.cancha_repo.get_all()
        
        # Filtrar por tipos de cancha si se especificaron
        if tipos_cancha:
            canchas = [c for c in canchas if c.id_tipo in tipos_cancha]
        
        horarios = self.horario_repo.get_all()
        max_turnos = len(canchas) * len(horarios)
        
        # Si tenemos número de equipos, limitar por simultaneidad
        if num_equipos is not None:
            max_simultaneos = num_equipos // 2
            # El máximo por día es: partidos simultáneos * cantidad de horarios
            max_por_equipos = max_simultaneos * len(horarios)
            return min(max_turnos, max_por_equipos)
        
        return max_turnos
    
    def calcular_total_partidos(self, num_equipos: int) -> int:
        """
        Calcula el total de partidos en un torneo todos contra todos
        Fórmula: n * (n-1) / 2
        """
        return (num_equipos * (num_equipos - 1)) // 2
    
    def calcular_dias_necesarios(self, total_partidos: int, partidos_por_dia: int) -> int:
        """Calcula cuántos días se necesitan para jugar todos los partidos"""
        import math
        return math.ceil(total_partidos / partidos_por_dia)
    
    def validar_disponibilidad_turnos(
        self, 
        fecha_inicio: date, 
        fecha_fin: date, 
        total_partidos: int,
        partidos_por_dia: int,
        num_equipos: int,
        tipos_cancha: List[int] = None
    ) -> dict:
        """
        Valida si hay suficientes turnos disponibles para el torneo SIN crear la reserva.
        Retorna diccionario con disponibilidad, monto exacto y mensaje.
        
        Usa el MISMO algoritmo de selección que crear_torneo_con_reserva para calcular
        el monto exacto que se cobrará.
        
        Útil para validar ANTES de procesar el pago.
        """
        from decimal import Decimal
        
        # Simular la selección de turnos usando el mismo algoritmo
        turnos_simulados = self.seleccionar_turnos_automaticos(
            fecha_inicio,
            fecha_fin,
            partidos_por_dia,
            total_partidos,
            num_equipos,
            tipos_cancha
        )
        
        total_disponibles = len(turnos_simulados)
        
        # Calcular monto EXACTO con los turnos que se seleccionarían
        monto_exacto = Decimal("0.00")
        for turno in turnos_simulados:
            monto_exacto += turno['precio']
        
        if total_disponibles < total_partidos:
            return {
                "disponible": False,
                "turnos_disponibles": total_disponibles,
                "turnos_necesarios": total_partidos,
                "monto_estimado": str(monto_exacto),
                "mensaje": f"No hay suficientes turnos disponibles. Se necesitan {total_partidos} pero solo hay {total_disponibles} disponibles"
            }
        
        return {
            "disponible": True,
            "turnos_disponibles": total_disponibles,
            "turnos_necesarios": total_partidos,
            "monto_estimado": str(monto_exacto),
            "mensaje": "Hay suficientes turnos disponibles"
        }
    
    def obtener_turnos_disponibles_por_fecha(self, fecha: date, tipos_cancha: List[int] = None) -> List[Tuple]:
        """
        Obtiene todos los turnos disponibles para una fecha específica
        Retorna lista de tuplas (id_turno, id_cancha, id_horario, nombre_cancha, hora_inicio, precio)
        
        Si se proporcionan tipos_cancha, solo retorna turnos de canchas de esos tipos
        """
        # Primero crear los turnos del día si no existen
        self._crear_turnos_del_dia(fecha, tipos_cancha)
        
        # Obtener todos los turnos disponibles de esa fecha
        turnos = self.turno_repo.get_by_fecha(fecha)
        turnos_info = []
        
        for turno in turnos:
            if turno.estado_nombre.lower() != "disponible":
                continue
            
            # Obtener información de la cancha
            cancha = self.cancha_repo.get_by_id(turno.id_cancha)
            if not cancha:
                continue
            
            # Filtrar por tipo de cancha si se especificó
            if tipos_cancha and cancha.id_tipo not in tipos_cancha:
                continue
            
            # Obtener tipo de cancha para el precio
            tipo_cancha = self.tipo_cancha_repo.get_by_id(cancha.id_tipo)
            if not tipo_cancha:
                continue
            
            # Calcular precio total (cancha + servicios)
            precio_total = tipo_cancha.precio_hora
            ids_servicios = self.cancha_servicio_repo.get_servicios_by_cancha(cancha.id_cancha)
            for id_servicio in ids_servicios:
                servicio = self.servicio_repo.get_by_id(id_servicio)
                if servicio:
                    precio_total += servicio.costo_servicio
            
            # Obtener horario
            horario = self.horario_repo.get_by_id(turno.id_horario)
            if not horario:
                continue
            
            turnos_info.append((
                turno.id_turno,
                turno.id_cancha,
                turno.id_horario,
                cancha.nombre,
                horario.hora_inicio,
                precio_total
            ))
        
        # Ordenar por horario (hora) y luego por cancha
        turnos_info.sort(key=lambda x: (x[4], x[1]))
        return turnos_info
    
    def seleccionar_turnos_automaticos(
        self, 
        fecha_inicio: date, 
        fecha_fin: date, 
        partidos_por_dia: int,
        total_partidos: int,
        num_equipos: int,
        tipos_cancha: List[int] = None
    ) -> List[dict]:
        """
        Selecciona automáticamente los turnos para el torneo
        Prioriza turnos simultáneos (mismo horario, diferentes canchas)
        sobre turnos consecutivos (misma cancha, diferentes horarios)
        
        IMPORTANTE: El máximo de partidos simultáneos es num_equipos // 2
        (cada partido requiere 2 equipos)
        
        Si se proporcionan tipos_cancha, solo selecciona turnos de canchas de esos tipos
        """
        turnos_seleccionados = []
        partidos_asignados = 0
        fecha_actual = fecha_inicio
        
        # Calcular máximo de partidos simultáneos
        max_simultaneos = num_equipos // 2
        
        while partidos_asignados < total_partidos and fecha_actual <= fecha_fin:
            turnos_dia = self.obtener_turnos_disponibles_por_fecha(fecha_actual, tipos_cancha)
            
            if not turnos_dia:
                # Si no hay turnos disponibles, pasar al siguiente día
                fecha_actual += timedelta(days=1)
                continue
            
            # Agrupar turnos por horario para priorizar simultaneidad
            turnos_por_horario = {}
            for turno in turnos_dia:
                hora = turno[4]  # hora_inicio
                if hora not in turnos_por_horario:
                    turnos_por_horario[hora] = []
                turnos_por_horario[hora].append(turno)
            
            # Seleccionar turnos priorizando simultaneidad pero respetando límite
            partidos_este_dia = 0
            horarios_ordenados = sorted(turnos_por_horario.keys())
            
            for hora in horarios_ordenados:
                turnos_disponibles = turnos_por_horario[hora]
                
                # Limitar cuántos turnos simultáneos se pueden tomar en este horario
                # No más de max_simultaneos ni de los que quedan por asignar
                turnos_en_este_horario = 0
                max_en_este_horario = min(
                    max_simultaneos,
                    partidos_por_dia - partidos_este_dia,
                    total_partidos - partidos_asignados
                )
                
                for turno in turnos_disponibles:
                    if turnos_en_este_horario >= max_en_este_horario:
                        break
                    
                    turnos_seleccionados.append({
                        'id_turno': turno[0],
                        'id_cancha': turno[1],
                        'id_horario': turno[2],
                        'nombre_cancha': turno[3],
                        'hora_inicio': turno[4],
                        'fecha': fecha_actual,
                        'precio': turno[5]
                    })
                    turnos_en_este_horario += 1
                    partidos_este_dia += 1
                    partidos_asignados += 1
                
                if partidos_este_dia >= partidos_por_dia or partidos_asignados >= total_partidos:
                    break
            
            fecha_actual += timedelta(days=1)
        
        return turnos_seleccionados
    
    def _crear_turnos_del_dia(self, fecha: date, tipos_cancha: List[int] = None):
        """Crea los turnos para un día específico si no existen
        
        Si se proporcionan tipos_cancha, solo crea turnos para canchas de esos tipos
        """
        canchas = self.cancha_repo.get_all()
        
        # Filtrar por tipos de cancha si se especificaron
        if tipos_cancha:
            canchas = [c for c in canchas if c.id_tipo in tipos_cancha]
        
        horarios = self.horario_repo.get_all()
        
        for cancha in canchas:
            for horario in horarios:
                # Verificar si ya existe el turno
                turno_existente = self.turno_repo.get_by_cancha_horario_fecha(
                    cancha.id_cancha, horario.id_horario, fecha
                )
                
                if not turno_existente:
                    # Crear el turno con estado disponible
                    nuevo_turno = Turno(
                        id_cancha=cancha.id_cancha,
                        id_horario=horario.id_horario,
                        fecha=fecha,
                        estado=TurnoDisponible()
                    )
                    self.turno_repo.create(nuevo_turno)
    
    def crear_torneo_con_reserva(self, data: TorneoReservaRequest) -> dict:
        """
        Crea un torneo completo con:
        1. El torneo en la BD
        2. Los equipos asociados
        3. Selección automática de turnos
        4. Reserva de los turnos
        5. Registro del pago
        
        Retorna información completa del torneo y los turnos seleccionados
        """
        # Validaciones iniciales
        num_equipos = len(data.equipos)
        if num_equipos < 2:
            raise ValueError("Se requieren al menos 2 equipos para crear un torneo")
        
        # Validar que los tipos de cancha existan
        for id_tipo in data.tipos_cancha:
            tipo = self.tipo_cancha_repo.get_by_id(id_tipo)
            if not tipo:
                raise ValueError(f"El tipo de cancha {id_tipo} no existe")
        
        total_partidos = data.total_partidos
        max_partidos_dia = self.calcular_max_partidos_por_dia(num_equipos, data.tipos_cancha)
        
        if data.partidos_por_dia > max_partidos_dia:
            raise ValueError(
                f"No se pueden jugar {data.partidos_por_dia} partidos por día. "
                f"Máximo disponible: {max_partidos_dia}"
            )
        
        dias_necesarios = self.calcular_dias_necesarios(total_partidos, data.partidos_por_dia)
        dias_disponibles = (data.fecha_fin - data.fecha_inicio).days + 1
        
        if dias_necesarios > dias_disponibles:
            raise ValueError(
                f"Se necesitan {dias_necesarios} días para {total_partidos} partidos "
                f"a {data.partidos_por_dia} por día, pero solo hay {dias_disponibles} días disponibles"
            )
        
        # Validar método de pago
        metodo_pago = self.metodo_pago_repo.get_by_id(data.id_metodo_pago)
        if not metodo_pago:
            raise ValueError(f"El método de pago {data.id_metodo_pago} no existe")
        
        # Determinar estado de la reserva según método de pago
        if "efectivo" in metodo_pago.descripcion.lower():
            estado_reserva = ReservaPendiente()
        else:
            estado_reserva = ReservaPagada()
        
        try:
            # Deshabilitar autocommit para manejar transacción
            self.torneo_repo.autocommit = False
            self.equipo_repo.autocommit = False
            self.reserva_repo.autocommit = False
            self.turno_repo.autocommit = False
            self.detalle_repo.autocommit = False
            self.pago_repo.autocommit = False
            
            # 1. Crear el torneo
            nuevo_torneo = Torneo(
                nombre=data.nombre_torneo,
                fecha_inicio=data.fecha_inicio,
                fecha_fin=data.fecha_fin
            )
            torneo_creado = self.torneo_repo.create(nuevo_torneo)
            
            # 2. Crear los equipos
            equipos_creados = []
            for equipo_data in data.equipos:
                nuevo_equipo = Equipo(
                    id_torneo=torneo_creado.id_torneo,
                    nombre=equipo_data.nombre,
                    cant_jugadores=equipo_data.cant_jugadores
                )
                equipo_creado = self.equipo_repo.create(nuevo_equipo)
                equipos_creados.append(equipo_creado)
            
            # 3. Seleccionar turnos automáticamente
            turnos_seleccionados = self.seleccionar_turnos_automaticos(
                data.fecha_inicio,
                data.fecha_fin,
                data.partidos_por_dia,
                total_partidos,
                num_equipos,
                data.tipos_cancha
            )
            
            if len(turnos_seleccionados) < total_partidos:
                raise ValueError(
                    f"No hay suficientes turnos disponibles. "
                    f"Se necesitan {total_partidos} pero solo hay {len(turnos_seleccionados)} disponibles"
                )
            
            # 4. Calcular monto total
            monto_total = Decimal("0.00")
            for turno in turnos_seleccionados:
                monto_total += turno['precio']
            
            # 5. Crear la reserva
            nueva_reserva = Reserva(
                id_cliente=data.id_cliente,
                id_torneo=torneo_creado.id_torneo,
                monto_total=monto_total,
                fecha_reserva=date.today(),
                estado=estado_reserva
            )
            reserva_creada = self.reserva_repo.create(nueva_reserva)
            
            # 6. Marcar turnos como no disponibles y crear detalles
            for turno_data in turnos_seleccionados:
                # Obtener el turno
                turno = self.turno_repo.get_by_id(turno_data['id_turno'])
                if turno:
                    # Cambiar estado a no disponible
                    turno.cambiar_estado(TurnoNoDisponible())
                    self.turno_repo.update(turno)
                    
                    # Crear detalle de reserva
                    detalle = ReservaDetalle(
                        id_reserva=reserva_creada.id_reserva,
                        id_turno=turno.id_turno,
                        precio_total_item=turno_data['precio']
                    )
                    self.detalle_repo.create(detalle)
            
            # 7. Registrar el pago
            nuevo_pago = Pago(
                id_reserva=reserva_creada.id_reserva,
                id_metodo_pago=data.id_metodo_pago,
                fecha_pago=date.today(),
                monto=monto_total
            )
            self.pago_repo.create(nuevo_pago)
            
            # Confirmar transacción
            self.connection.commit()
            
            # Preparar respuesta
            return {
                'id_torneo': torneo_creado.id_torneo,
                'id_reserva': reserva_creada.id_reserva,
                'nombre_torneo': torneo_creado.nombre,
                'fecha_inicio': torneo_creado.fecha_inicio,
                'fecha_fin': torneo_creado.fecha_fin,
                'equipos': [{'nombre': eq.nombre, 'cant_jugadores': eq.cant_jugadores} for eq in equipos_creados],
                'turnos_seleccionados': turnos_seleccionados,
                'total_partidos': total_partidos,
                'partidos_por_dia': data.partidos_por_dia,
                'max_partidos_por_dia': max_partidos_dia,
                'monto_total': str(monto_total),
                'dias_necesarios': dias_necesarios
            }
            
        except Exception as e:
            self.connection.rollback()
            raise e
        
        finally:
            # Restaurar autocommit
            self.torneo_repo.autocommit = True
            self.equipo_repo.autocommit = True
            self.reserva_repo.autocommit = True
            self.turno_repo.autocommit = True
            self.detalle_repo.autocommit = True
            self.pago_repo.autocommit = True
