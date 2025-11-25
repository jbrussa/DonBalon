import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ReservationConfirmation from './TournamentConfirmation';
import './Tournament.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function Tournament({ onClose }) {
    const { user } = useAuth();

    // Datos del torneo
    const [nombreTorneo, setNombreTorneo] = useState('');
    const [fechaInicio, setFechaInicio] = useState('');
    const [fechaFin, setFechaFin] = useState('');

    // Equipos
    const [equipos, setEquipos] = useState([]);
    const [nuevoEquipoNombre, setNuevoEquipoNombre] = useState('');
    const [nuevoEquipoJugadores, setNuevoEquipoJugadores] = useState('');

    // Configuración de partidos
    const [maxPartidosDia, setMaxPartidosDia] = useState(0);
    const [partidosPorDia, setPartidosPorDia] = useState(1);
    const [totalPartidos, setTotalPartidos] = useState('');
    const [diasNecesarios, setDiasNecesarios] = useState(0);

    // Tipos de cancha
    const [tiposCancha, setTiposCancha] = useState([]);
    const [tiposCanchaSeleccionados, setTiposCanchaSeleccionados] = useState([]);

    // Métodos de pago
    const [metodosPago, setMetodosPago] = useState([]);
    const [metodoPagoSeleccionado, setMetodoPagoSeleccionado] = useState('');

    // Estados del flujo
    const [paso, setPaso] = useState(1); // 1: datos, 2: confirmación, 3: pago procesado
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [resultado, setResultado] = useState(null);
    const [montoTotal, setMontoTotal] = useState(0);

    // Información para tarjeta
    const [numeroTarjeta, setNumeroTarjeta] = useState('');
    const [nombreTitular, setNombreTitular] = useState('');
    const [fechaVencimiento, setFechaVencimiento] = useState('');
    const [cvv, setCvv] = useState('');

    // Cargar métodos de pago y tipos de cancha
    useEffect(() => {

        fetch(`${API_BASE}/metodos-pago`)
            .then(res => res.json())
            .then(data => {
                setMetodosPago(data);
                if (data.length > 0) {
                    setMetodoPagoSeleccionado(data[0].id_metodo_pago);
                }
            })
            .catch(err => console.error('Error al obtener métodos de pago:', err));

        fetch(`${API_BASE}/tipos-cancha`)
            .then(res => res.json())
            .then(data => {
                setTiposCancha(data);
                // Seleccionar todos por defecto
                setTiposCanchaSeleccionados(data.map(t => t.id_tipo));
            })
            .catch(err => console.error('Error al obtener tipos de cancha:', err));
    }, []);

    // Recalcular máximo de partidos cuando cambian los equipos o tipos de cancha
    useEffect(() => {
        if (equipos.length >= 2 && tiposCanchaSeleccionados.length > 0) {
            const numEquipos = equipos.length;
            const tiposParam = tiposCanchaSeleccionados.join(',');
            fetch(`${API_BASE}/torneos/max-partidos-dia?num_equipos=${numEquipos}&tipos_cancha=${tiposParam}`)
                .then(res => res.json())
                .then(data => {
                    setMaxPartidosDia(data.max_partidos_por_dia);
                })
                .catch(err => console.error('Error al obtener max partidos:', err));
        } else if (tiposCanchaSeleccionados.length > 0) {
            // Si hay menos de 2 equipos, obtener el máximo general con tipos de cancha
            const tiposParam = tiposCanchaSeleccionados.join(',');
            fetch(`${API_BASE}/torneos/max-partidos-dia?tipos_cancha=${tiposParam}`)
                .then(res => res.json())
                .then(data => {
                    setMaxPartidosDia(data.max_partidos_por_dia);
                })
                .catch(err => console.error('Error al obtener max partidos:', err));
        }
    }, [equipos, tiposCanchaSeleccionados]);

    // Calcular días necesarios
    useEffect(() => {
        const partidos = parseInt(totalPartidos) || 0;
        if (partidos > 0 && partidosPorDia > 0) {
            const dias = Math.ceil(partidos / partidosPorDia);
            setDiasNecesarios(dias);
        } else {
            setDiasNecesarios(0);
        }
    }, [totalPartidos, partidosPorDia]);

    const agregarEquipo = () => {
        if (!nuevoEquipoNombre.trim()) {
            alert('Debe ingresar el nombre del equipo');
            return;
        }

        // Validar que no exista un equipo con el mismo nombre
        const nombreExistente = equipos.find(
            eq => eq.nombre.toLowerCase().trim() === nuevoEquipoNombre.toLowerCase().trim()
        );
        if (nombreExistente) {
            alert('Ya existe un equipo con ese nombre en este torneo');
            return;
        }

        const jugadores = parseInt(nuevoEquipoJugadores);
        if (!jugadores || jugadores < 5) {
            alert('Debe ingresar al menos 5 jugadores por equipo');
            return;
        }

        setEquipos([...equipos, {
            nombre: nuevoEquipoNombre.trim(),
            cant_jugadores: jugadores
        }]);

        setNuevoEquipoNombre('');
        setNuevoEquipoJugadores('');
    };

    const eliminarEquipo = (index) => {
        setEquipos(equipos.filter((_, i) => i !== index));
    };

    const toggleTipoCancha = (idTipo) => {
        if (tiposCanchaSeleccionados.includes(idTipo)) {
            // Desmarcar solo si hay al menos otro seleccionado
            if (tiposCanchaSeleccionados.length > 1) {
                setTiposCanchaSeleccionados(tiposCanchaSeleccionados.filter(id => id !== idTipo));
            } else {
                alert('Debe seleccionar al menos un tipo de cancha');
            }
        } else {
            // Marcar
            setTiposCanchaSeleccionados([...tiposCanchaSeleccionados, idTipo]);
        }
    };

    const validarDatos = () => {
        if (!nombreTorneo.trim()) {
            setError('Debe ingresar el nombre del torneo');
            return false;
        }

        if (!fechaInicio || !fechaFin) {
            setError('Debe seleccionar las fechas del torneo');
            return false;
        }

        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        const inicio = new Date(fechaInicio + 'T00:00:00');
        const fin = new Date(fechaFin + 'T00:00:00');

        if (inicio < hoy) {
            setError('La fecha de inicio no puede ser anterior a la fecha actual');
            return false;
        }

        if (fin < inicio) {
            setError('La fecha de fin debe ser mayor o igual a la fecha de inicio');
            return false;
        }

        if (equipos.length < 2) {
            setError('Debe ingresar al menos 2 equipos');
            return false;
        }

        if (tiposCanchaSeleccionados.length === 0) {
            setError('Debe seleccionar al menos un tipo de cancha');
            return false;
        }

        const partidos = parseInt(totalPartidos) || 0;
        if (partidos < 1) {
            setError('Debe ingresar la cantidad total de partidos del torneo');
            return false;
        }

        if (partidosPorDia < 1) {
            setError('Los partidos por día deben ser al menos 1');
            return false;
        }

        // Validar que no exceda el máximo disponible
        if (partidosPorDia > maxPartidosDia) {
            setError(`No se pueden jugar ${partidosPorDia} partidos por día. Máximo disponible: ${maxPartidosDia}`);
            return false;
        }

        const diasDisponibles = Math.floor((fin - inicio) / (1000 * 60 * 60 * 24)) + 1;
        if (diasNecesarios > diasDisponibles) {
            setError(
                `Se necesitan ${diasNecesarios} días para ${partidos} partidos ` +
                `a ${partidosPorDia} por día, pero solo hay ${diasDisponibles} días disponibles`
            );
            return false;
        }

        return true;
    };

    const handleContinuar = async () => {
        setError('');

        if (!validarDatos()) {
            return;
        }

        setLoading(true);

        try {
            // Validar disponibilidad de turnos ANTES de ir al pago
            const tiposParam = tiposCanchaSeleccionados.join(',');
            const numEquipos = equipos.length;
            const response = await fetch(
                `${API_BASE}/torneos/validar-disponibilidad?` +
                `fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}&` +
                `total_partidos=${parseInt(totalPartidos)}&partidos_por_dia=${partidosPorDia}&` +
                `num_equipos=${numEquipos}&` +
                `tipos_cancha=${tiposParam}`
            );

            if (!response.ok) {
                throw new Error('Error al validar disponibilidad');
            }

            const validacion = await response.json();

            if (!validacion.disponible) {
                setError(validacion.mensaje);
                setLoading(false);
                return;
            }

            // Guardar el monto total estimado
            setMontoTotal(parseFloat(validacion.monto_estimado || 0));

            // Si hay turnos disponibles, continuar al paso de pago
            setPaso(2);

        } catch (err) {
            setError(err.message || 'Error al validar disponibilidad de turnos');
        } finally {
            setLoading(false);
        }
    };

    const handleConfirmarPago = async () => {
        setError('');
        setLoading(true);

        // Validar datos de tarjeta si es necesario
        const metodoPago = metodosPago.find(m => m.id_metodo_pago === parseInt(metodoPagoSeleccionado));
        if (metodoPago && metodoPago.descripcion.toLowerCase().includes('tarjeta')) {
            if (!numeroTarjeta || !nombreTitular || !fechaVencimiento || !cvv) {
                setError('Debe completar todos los datos de la tarjeta');
                setLoading(false);
                return;
            }

            // Validar formato de número de tarjeta (16 dígitos)
            const numeroLimpio = numeroTarjeta.replace(/\s/g, '');
            if (!/^\d{16}$/.test(numeroLimpio)) {
                setError('El número de tarjeta debe tener 16 dígitos');
                setLoading(false);
                return;
            }

            // Validar formato de CVV (3 dígitos)
            if (!/^\d{3}$/.test(cvv)) {
                setError('El CVV debe tener 3 dígitos');
                setLoading(false);
                return;
            }

            // Validar formato de fecha de vencimiento (MM/AAAA)
            if (!/^\d{2}\/\d{4}$/.test(fechaVencimiento)) {
                setError('La fecha de vencimiento debe tener el formato MM/AAAA');
                setLoading(false);
                return;
            }

            // Validar que la fecha sea posterior a la actual
            const [mes, anio] = fechaVencimiento.split('/').map(num => parseInt(num));
            const hoy = new Date();
            const mesActual = hoy.getMonth() + 1;
            const anioActual = hoy.getFullYear();

            if (mes < 1 || mes > 12) {
                setError('El mes debe estar entre 01 y 12');
                setLoading(false);
                return;
            }

            if (anio < anioActual || (anio === anioActual && mes < mesActual)) {
                setError('La tarjeta está vencida');
                setLoading(false);
                return;
            }
        }

        try {
            // Validar que todos los datos requeridos estén presentes
            if (!totalPartidos || isNaN(parseInt(totalPartidos))) {
                setError('Debe ingresar la cantidad total de partidos');
                setLoading(false);
                return;
            }

            if (!tiposCanchaSeleccionados || tiposCanchaSeleccionados.length === 0) {
                setError('Debe seleccionar al menos un tipo de cancha');
                setLoading(false);
                return;
            }

            const response = await fetch(`${API_BASE}/torneos/reservar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id_cliente: user.id_cliente,
                    nombre_torneo: nombreTorneo,
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    equipos: equipos,
                    total_partidos: parseInt(totalPartidos),
                    partidos_por_dia: parseInt(partidosPorDia),
                    id_metodo_pago: parseInt(metodoPagoSeleccionado),
                    tipos_cancha: tiposCanchaSeleccionados
                })
            });

            if (!response.ok) {
                let errorMessage = 'Error al crear el torneo';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch {
                    errorMessage = `Error del servidor (${response.status}): ${response.statusText}`;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            setResultado(data);
            setPaso(3);

        } catch (err) {
            console.error('Error completo:', err);
            setError(err.message || 'Error desconocido al crear el torneo');
        } finally {
            setLoading(false);
        }
    };

    const handleVolver = () => {
        setPaso(1);
    };

    const handleCerrar = () => {
        if (paso === 3) {
            // Si se completó el pago, recargar la página o actualizar datos
            window.location.reload();
        } else {
            onClose();
        }
    };

    // Función para formatear número de tarjeta (agregar espacios cada 4 dígitos)
    const formatearNumeroTarjeta = (valor) => {
        const numeros = valor.replace(/\s/g, '').replace(/\D/g, '');
        const grupos = numeros.match(/.{1,4}/g);
        return grupos ? grupos.join(' ') : numeros;
    };

    const handleNumeroTarjetaChange = (e) => {
        const valor = e.target.value;
        const soloNumeros = valor.replace(/\D/g, '');
        if (soloNumeros.length <= 16) {
            setNumeroTarjeta(formatearNumeroTarjeta(soloNumeros));
        }
    };

    // Función para formatear fecha de vencimiento (MM/AAAA)
    const handleFechaVencimientoChange = (e) => {
        let valor = e.target.value.replace(/\D/g, '');

        if (valor.length >= 2) {
            valor = valor.slice(0, 2) + '/' + valor.slice(2, 6);
        }

        setFechaVencimiento(valor);
    };

    // Función para permitir solo números en CVV
    const handleCvvChange = (e) => {
        const valor = e.target.value.replace(/\D/g, '');
        if (valor.length <= 3) {
            setCvv(valor);
        }
    };

    const metodoPago = metodosPago.find(m => m.id_metodo_pago === parseInt(metodoPagoSeleccionado));
    const esTarjeta = metodoPago && metodoPago.descripcion.toLowerCase().includes('tarjeta');

    return (
        <div className="tournament-modal-overlay" onClick={handleCerrar}>
            <div className="tournament-modal" onClick={(e) => e.stopPropagation()}>
                <button className="tournament-close" onClick={handleCerrar}>✕</button>

                {paso === 1 && (
                    <div className="tournament-form">
                        <h2>Crear Torneo</h2>

                        {error && <div className="tournament-error">{error}</div>}

                        {/* Datos del torneo */}
                        <div className="tournament-section">
                            <h3>Datos del Torneo</h3>

                            <div className="tournament-field">
                                <label>Nombre del Torneo</label>
                                <input
                                    type="text"
                                    value={nombreTorneo}
                                    onChange={(e) => setNombreTorneo(e.target.value)}
                                    placeholder="Ej: Torneo de Verano 2025"
                                    maxLength={100}
                                />
                            </div>

                            <div className="tournament-dates">
                                <div className="tournament-field">
                                    <label>Fecha de Inicio</label>
                                    <input
                                        type="date"
                                        value={fechaInicio}
                                        onChange={(e) => setFechaInicio(e.target.value)}
                                        min={new Date().toISOString().split('T')[0]}
                                    />
                                </div>

                                <div className="tournament-field">
                                    <label>Fecha de Fin</label>
                                    <input
                                        type="date"
                                        value={fechaFin}
                                        onChange={(e) => setFechaFin(e.target.value)}
                                        min={fechaInicio || new Date().toISOString().split('T')[0]}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Equipos */}
                        <div className="tournament-section">
                            <h3>Equipos Participantes</h3>

                            <div className="tournament-add-team">
                                <input
                                    type="text"
                                    value={nuevoEquipoNombre}
                                    onChange={(e) => setNuevoEquipoNombre(e.target.value)}
                                    placeholder="Nombre del equipo"
                                    maxLength={50}
                                />
                                <input
                                    type="number"
                                    value={nuevoEquipoJugadores}
                                    onChange={(e) => setNuevoEquipoJugadores(e.target.value)}
                                    placeholder="Jugadores"
                                    min="1"
                                />
                                <button onClick={agregarEquipo} className="btn-add-team">
                                    Agregar
                                </button>
                            </div>

                            {equipos.length > 0 && (
                                <div className="tournament-teams-list">
                                    {equipos.map((equipo, index) => (
                                        <div key={index} className="tournament-team-item">
                                            <div className="team-info">
                                                <span className="team-name">{equipo.nombre}</span>
                                                <span className="team-players">{equipo.cant_jugadores} jugadores</span>
                                            </div>
                                            <button
                                                onClick={() => eliminarEquipo(index)}
                                                className="btn-remove-team"
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Tipos de Cancha */}
                        <div className="tournament-section">
                            <h3>Tipos de Cancha</h3>
                            <p className="section-description">
                                Seleccione uno o más tipos de cancha para el torneo
                            </p>

                            <div className="tipos-cancha-list">
                                {tiposCancha.map(tipo => (
                                    <div key={tipo.id_tipo} className="tipo-cancha-item">
                                        <label className="checkbox-label">
                                            <input
                                                type="checkbox"
                                                checked={tiposCanchaSeleccionados.includes(tipo.id_tipo)}
                                                onChange={() => toggleTipoCancha(tipo.id_tipo)}
                                            />
                                            <span className="tipo-cancha-info">
                                                <span className="tipo-nombre">{tipo.descripcion}</span>
                                                <span className="tipo-precio">${parseFloat(tipo.precio_hora).toFixed(2)}/hora</span>
                                            </span>
                                        </label>
                                    </div>
                                ))}
                            </div>

                            {tiposCanchaSeleccionados.length === 0 && (
                                <small className="warning-text">Debe seleccionar al menos un tipo de cancha</small>
                            )}
                        </div>

                        {/* Configuración de partidos */}
                        {equipos.length >= 2 && (
                            <div className="tournament-section">
                                <h3>Configuración de Partidos</h3>

                                <div className="tournament-field">
                                    <label>Total de partidos del torneo</label>
                                    <input
                                        type="number"
                                        value={totalPartidos}
                                        onChange={(e) => setTotalPartidos(e.target.value)}
                                        placeholder="Ingrese cantidad de partidos"
                                        min="1"
                                    />
                                    <small>Ingrese la cantidad total según el formato del torneo</small>
                                </div>

                                {parseInt(totalPartidos) > 0 && (
                                    <>
                                        <div className="tournament-field">
                                            <label>Partidos que desea jugar por día como máximo</label>
                                            <input
                                                type="number"
                                                value={partidosPorDia}
                                                onChange={(e) => setPartidosPorDia(parseInt(e.target.value) || 1)}
                                                min="1"
                                            />
                                            <small>Días necesarios: {diasNecesarios}</small>
                                        </div>
                                    </>
                                )}
                            </div>
                        )}

                        <div className="tournament-actions">
                            <button onClick={handleCerrar} className="btn-cancel">
                                Cancelar
                            </button>
                            <button onClick={handleContinuar} className="btn-continue">
                                Continuar
                            </button>
                        </div>
                    </div>
                )}

                {paso === 2 && (
                    <div className="tournament-payment">
                        <h2>Confirmar Reserva del Torneo</h2>

                        {error && <div className="tournament-error">{error}</div>}

                        {/* Resumen del torneo */}
                        <div className="tournament-summary">
                            <h3>{nombreTorneo}</h3>
                            <div className="summary-dates">
                                Del {new Date(fechaInicio + 'T00:00:00').toLocaleDateString()} al {new Date(fechaFin + 'T00:00:00').toLocaleDateString()}
                            </div>

                            <div className="summary-section">
                                <h4>Equipos ({equipos.length})</h4>
                                <ul>
                                    {equipos.map((equipo, index) => (
                                        <li key={index}>
                                            {equipo.nombre} - {equipo.cant_jugadores} jugadores
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="summary-section">
                                <h4>Información de Partidos</h4>
                                <div className="summary-stats">
                                    <div>Total de partidos: <strong>{totalPartidos}</strong></div>
                                    <div>Partidos por día: <strong>{partidosPorDia}</strong></div>
                                    <div>Días necesarios: <strong>{diasNecesarios}</strong></div>
                                </div>
                            </div>
                        </div>

                        {/* Método de pago */}
                        <div className="payment-method-section">
                            <h3>Método de Pago</h3>
                            <select
                                value={metodoPagoSeleccionado}
                                onChange={(e) => setMetodoPagoSeleccionado(e.target.value)}
                            >
                                {metodosPago.map(metodo => (
                                    <option key={metodo.id_metodo_pago} value={metodo.id_metodo_pago}>
                                        {metodo.descripcion}
                                    </option>
                                ))}
                            </select>

                            {esTarjeta && (
                                <div className="card-details">
                                    <div className="tournament-field">
                                        <label>Número de Tarjeta</label>
                                        <input
                                            type="text"
                                            value={numeroTarjeta}
                                            onChange={handleNumeroTarjetaChange}
                                            placeholder="1234 5678 9012 3456"
                                            maxLength={19}
                                        />
                                        <small>16 dígitos</small>
                                    </div>
                                    <div className="tournament-field">
                                        <label>Nombre del Titular</label>
                                        <input
                                            type="text"
                                            value={nombreTitular}
                                            onChange={(e) => setNombreTitular(e.target.value)}
                                            placeholder="Nombre completo"
                                        />
                                    </div>
                                    <div className="card-extra">
                                        <div className="tournament-field">
                                            <label>Vencimiento</label>
                                            <input
                                                type="text"
                                                value={fechaVencimiento}
                                                onChange={handleFechaVencimientoChange}
                                                placeholder="MM/AAAA"
                                                maxLength={7}
                                            />
                                        </div>
                                        <div className="tournament-field">
                                            <label>CVV</label>
                                            <input
                                                type="text"
                                                value={cvv}
                                                onChange={handleCvvChange}
                                                placeholder="123"
                                                maxLength={3}
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Monto Total */}
                        <div className="payment-total-section">
                            <div className="total-amount">
                                <span className="total-label">Total a Pagar:</span>
                                <span className="total-value">${montoTotal.toFixed(2)}</span>
                            </div>
                            <small className="total-note">Monto estimado según turnos disponibles</small>
                        </div>

                        <div className="tournament-actions">
                            <button onClick={handleVolver} className="btn-cancel" disabled={loading}>
                                Volver
                            </button>
                            <button onClick={handleConfirmarPago} className="btn-pay" disabled={loading}>
                                {loading ? 'Procesando...' : 'Confirmar y Pagar'}
                            </button>
                        </div>
                    </div>
                )}

                {paso === 3 && resultado && (
                    <ReservationConfirmation
                        resultado={resultado}
                        onClose={handleCerrar}
                    />
                )}
            </div>
        </div>
    );
}
