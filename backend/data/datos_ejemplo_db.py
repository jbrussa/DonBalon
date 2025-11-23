import sqlite3
from pathlib import Path

def insert_sample_data(db_path):
    """
    Inserta datos de ejemplo en la base de datos
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    try:
        # Estado
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('Disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('No disponible', 'turno')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PENDIENTE', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('PAGADA', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('FINALIZADA', 'reserva')")
        cursor.execute("INSERT INTO Estado (nombre, ambito) VALUES ('CANCELADA', 'reserva')")
        
        # TipoCancha
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Futbol', 500.00)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Basquet', 400.00)")
        cursor.execute("INSERT INTO TipoCancha (descripcion, precio_hora) VALUES ('Tenis', 300.00)")
        
        # Cancha
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (1, 'Cancha 1')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (1, 'Cancha 2')")
        cursor.execute("INSERT INTO Cancha (id_tipo, nombre) VALUES (2, 'Cancha 3')")
        
        # Servicio
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Agua', 50.00)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Bebidas', 100.00)")
        cursor.execute("INSERT INTO Servicio (descripcion, costo_servicio) VALUES ('Arbitro', 150.00)")
        
        # CanchaServicio
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (1, 1)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (2, 2)")
        cursor.execute("INSERT INTO CanchaServicio (id_cancha, id_servicio) VALUES (3, 1)")
        
        # Horario
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('09:00', '10:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('10:00', '11:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('14:00', '15:00')")
        cursor.execute("INSERT INTO Horario (hora_inicio, hora_fin) VALUES ('15:00', '16:00')")
        
        # Turno
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (1, 1, '2025-11-20', 'DISPONIBLE')")
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (1, 2, '2025-11-20', 'DISPONIBLE')")
        cursor.execute("INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (2, 1, '2025-11-20', 'NO DISPONIBLE')")
        
        # Cliente
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (1, 'Juan', 'Perez', '1234567890', 'juan@example.com', 'pass123', 1)")
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (2, 'Maria', 'Garcia', '0987654321', 'maria@example.com', 'pass456', 0)")
        cursor.execute("INSERT INTO Cliente (id_cliente, nombre, apellido, telefono, mail, password, admin) VALUES (3, 'Carlos', 'Lopez', '1122334455', 'carlos@example.com', 'pass789', 0)")
        
        
        # MetodoPago
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Tarjeta')")
        cursor.execute("INSERT INTO MetodoPago (descripcion) VALUES ('Efectivo')")
        
        # Torneo
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Copa Local', '2025-11-20', '2025-12-20')""")
        cursor.execute("""INSERT INTO Torneo (nombre, fecha_inicio, fecha_fin) 
                         VALUES ('Campeonato Regional', '2025-12-01', '2025-12-31')""")
        
        # Equipo
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Abuela Lala', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (1, 'Monte Maiz', 11)")
        cursor.execute("INSERT INTO Equipo (id_torneo, nombre, cant_jugadores) VALUES (2, 'Belgrano', 11)")
        
        # Reserva
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (1, 500.00, '2025-11-20', 'PENDIENTE')""")
        cursor.execute("""INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva)
                         VALUES (2, 500.00, '2025-11-20', 'PAGADA')""")
        
        # ReservaDetalle
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (1, 1, 500.00)""")
        cursor.execute("""INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item)
                         VALUES (2, 2, 450.00)""")
        
        # Pago
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto)
                         VALUES (1, 1, '2025-11-20', 500.00)""")
        cursor.execute("""INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto)
                         VALUES (2, 1, '2025-11-20', 450.00)""")
        
        conn.commit()
        print(" Datos de ejemplo insertados exitosamente")
        
    except sqlite3.Error as e:
        print(f" Error al insertar datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = Path(__file__).parent / "donbalon.db"
    insert_sample_data(db_path)

