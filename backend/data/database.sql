-- Base de datos SQLite para DonBalon - Sistema de Gestión de Reservas de Canchas Deportivas
-- Diagrama de Entidad-Relación (DER) de Canchas Deportivas

-- Tabla: Estado
CREATE TABLE IF NOT EXISTS Estado (
    id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    ambito VARCHAR(50) NOT NULL
);

-- Tabla: TipoCancha
CREATE TABLE IF NOT EXISTS TipoCancha (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    precio_hora DECIMAL(10, 2) NOT NULL
);

-- Tabla: Cancha
CREATE TABLE IF NOT EXISTS Cancha (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tipo INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_tipo) REFERENCES TipoCancha(id_tipo)
);

-- Tabla: Servicio
CREATE TABLE IF NOT EXISTS Servicio (
    id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    costo_servicio DECIMAL(10, 2) NOT NULL
);

-- Tabla: CanchaServicio (tabla de asociación)
CREATE TABLE IF NOT EXISTS CanchaServicio (
    id_cancha INTEGER NOT NULL,
    id_servicio INTEGER NOT NULL,
    PRIMARY KEY (id_cancha, id_servicio),
    FOREIGN KEY (id_cancha) REFERENCES Cancha(id_cancha),
    FOREIGN KEY (id_servicio) REFERENCES Servicio(id_servicio)
);

-- Tabla: Horario
CREATE TABLE IF NOT EXISTS Horario (
    id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- Tabla: Turno
CREATE TABLE IF NOT EXISTS Turno (
    id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cancha INTEGER NOT NULL,
    id_horario INTEGER NOT NULL,
    fecha DATE NOT NULL,
    id_estado INTEGER NOT NULL,
    FOREIGN KEY (id_cancha) REFERENCES Cancha(id_cancha),
    FOREIGN KEY (id_horario) REFERENCES Horario(id_horario),
    FOREIGN KEY (id_estado) REFERENCES Estado(id_estado)
);

-- Tabla: Cliente
CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(30) NOT NULL,
    mail VARCHAR(100) NOT NULL
);

-- Tabla: MetodoPago
CREATE TABLE IF NOT EXISTS MetodoPago (
    id_metodo_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla: Pago
CREATE TABLE IF NOT EXISTS Pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reserva INTEGER NOT NULL,
    id_metodo_pago INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    estado_pago VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_reserva) REFERENCES Reserva(id_reserva),
    FOREIGN KEY (id_metodo_pago) REFERENCES MetodoPago(id_metodo_pago)
);

-- Tabla: Reserva
CREATE TABLE IF NOT EXISTS Reserva (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,
    fecha_reserva DATE NOT NULL,
    estado_reserva VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

-- Tabla: ReservaDetalle (relación de muchos a muchos entre Reserva y Turno)
CREATE TABLE IF NOT EXISTS ReservaDetalle (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reserva INTEGER NOT NULL,
    id_turno INTEGER NOT NULL,
    precio_total_item DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_reserva) REFERENCES Reserva(id_reserva),
    FOREIGN KEY (id_turno) REFERENCES Turno(id_turno)
);

-- Tabla: Torneo
CREATE TABLE IF NOT EXISTS Torneo (
    id_torneo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

-- Tabla: Equipo
CREATE TABLE IF NOT EXISTS Equipo (
    id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneo INTEGER NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    cant_jugadores INTEGER NOT NULL,
    FOREIGN KEY (id_torneo) REFERENCES Torneo(id_torneo)
);

-- Índices para mejorar las búsquedas
-- Índices para mejorar las búsquedas
CREATE INDEX IF NOT EXISTS idx_cancha_tipo ON Cancha(id_tipo);
CREATE INDEX IF NOT EXISTS idx_turno_cancha ON Turno(id_cancha);
CREATE INDEX IF NOT EXISTS idx_turno_horario ON Turno(id_horario);
CREATE INDEX IF NOT EXISTS idx_turno_estado ON Turno(id_estado);
CREATE INDEX IF NOT EXISTS idx_pago_reserva ON Pago(id_reserva);
CREATE INDEX IF NOT EXISTS idx_pago_metodo ON Pago(id_metodo_pago);
CREATE INDEX IF NOT EXISTS idx_reserva_cliente ON Reserva(id_cliente);
CREATE INDEX IF NOT EXISTS idx_reserva_detalle_reserva ON ReservaDetalle(id_reserva);
CREATE INDEX IF NOT EXISTS idx_reserva_detalle_turno ON ReservaDetalle(id_turno);
CREATE INDEX IF NOT EXISTS idx_equipo_torneo ON Equipo(id_torneo);
