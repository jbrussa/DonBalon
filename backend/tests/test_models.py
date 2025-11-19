import os
import sys
import datetime
from decimal import Decimal

# Asegurarnos de que el root del proyecto esté en sys.path (este test está en backend/tests)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Algunos archivos y paquetes fueron creados bajo backend/, asegurarnos de añadirlo también
BACKEND_DIR = os.path.abspath(os.path.join(ROOT, 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from classes.cliente import Cliente, from_dict as cliente_from_dict
from classes.tipo_pago import TipoPago, from_dict as tipo_pago_from_dict
from classes.metodo_pago import MetodoPago, from_dict as metodo_pago_from_dict
from classes.pago import Pago, from_dict as pago_from_dict
from classes.reserva import Reserva, from_dict as reserva_from_dict
from classes.reserva_detalle import ReservaDetalle, from_dict as reserva_detalle_from_dict
from classes.torneo import Torneo, from_dict as torneo_from_dict
from classes.equipo import Equipo, from_dict as equipo_from_dict
from classes.cancha import Cancha, from_dict as cancha_from_dict
from classes.estado import Estado, from_dict as estado_from_dict
from classes.tipo_cancha import TipoCancha, from_dict as tipo_cancha_from_dict
from classes.turno import Turno, from_dict as turno_from_dict
from classes.horario import Horario, from_dict as horario_from_dict
from classes.servicio import Servicio, from_dict as servicio_from_dict
from classes.cancha_servicio import CanchaServicio, from_dict as cancha_servicio_from_dict


def roundtrip(factory, instance):
    d = instance.to_dict()
    new = factory(d)
    assert new == instance


def test_models_roundtrip():
    cliente = Cliente(1, "Juan", "Perez", "12345678", "1234", "a@b.com")
    tipo_pago = TipoPago(1, "Efectivo")
    metodo_pago = MetodoPago(1, "Tarjeta")
    pago = Pago(1, 10, 1, datetime.date(2025, 1, 2), Decimal("150.50"), "OK")
    reserva = Reserva(2, 1, 3, Decimal("200.00"), datetime.date(2025, 2, 3), "PEND")
    reserva_detalle = ReservaDetalle(1, 2, 3, 4, Decimal("100.00"), Decimal("80.00"), Decimal("180.00"))
    torneo = Torneo(1, "Copa", datetime.date(2025, 3, 1), datetime.date(2025, 3, 10))
    equipo = Equipo(1, 1, "Equipo A", 11)
    cancha = Cancha(1, 1, 1, "Cancha 1")
    estado = Estado(1, "Disponible")
    tipo_cancha = TipoCancha(1, "Futbol", Decimal("500.00"))
    turno = Turno(1, 1, 2, datetime.date(2025, 4, 4))
    horario = Horario(1, datetime.time(9, 0), datetime.time(10, 0))
    servicio = Servicio(1, "Agua", Decimal("50.00"))
    cancha_servicio = CanchaServicio(1, 1)

    roundtrip(cliente_from_dict, cliente)
    roundtrip(tipo_pago_from_dict, tipo_pago)
    roundtrip(metodo_pago_from_dict, metodo_pago)
    roundtrip(pago_from_dict, pago)
    roundtrip(reserva_from_dict, reserva)
    roundtrip(reserva_detalle_from_dict, reserva_detalle)
    roundtrip(torneo_from_dict, torneo)
    roundtrip(equipo_from_dict, equipo)
    roundtrip(cancha_from_dict, cancha)
    roundtrip(estado_from_dict, estado)
    roundtrip(tipo_cancha_from_dict, tipo_cancha)
    roundtrip(turno_from_dict, turno)
    roundtrip(horario_from_dict, horario)
    roundtrip(servicio_from_dict, servicio)
    roundtrip(cancha_servicio_from_dict, cancha_servicio)
