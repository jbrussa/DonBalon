import React, { useState } from 'react';
import './ReservationManager.css';

const ReservationManager = ({ onClose }) => {
    const [searchType, setSearchType] = useState('id'); // 'id', 'email', 'turno'

    // Estados para búsqueda por ID
    const [idReserva, setIdReserva] = useState('');

    // Estados para búsqueda por email
    const [emailCliente, setEmailCliente] = useState('');
    const [reservasCliente, setReservasCliente] = useState([]);

    // Estados para búsqueda por turno
    const [turnoData, setTurnoData] = useState({
        id_cancha: '',
        id_horario: '',
        fecha: ''
    });

    // Estados comunes
    const [reserva, setReserva] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [showConfirmDelete, setShowConfirmDelete] = useState(false);
    const [showConfirmPago, setShowConfirmPago] = useState(false);

    const handleBuscar = async () => {
        if (!idReserva.trim()) {
            setError('Por favor ingresa un ID de reserva');
            return;
        }

        setLoading(true);
        setError('');
        setReserva(null);
        setReservasCliente([]);
        setMensaje('');

        try {
            const response = await fetch(`http://localhost:8000/reservas/${idReserva}/detalles`);

            if (response.ok) {
                const data = await response.json();
                setReserva(data);
            } else if (response.status === 404) {
                setError('No se encontró una reserva con ese ID');
            } else {
                setError('Error al buscar la reserva');
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleBuscarPorEmail = async () => {
        if (!emailCliente.trim()) {
            setError('Por favor ingresa un email');
            return;
        }

        setLoading(true);
        setError('');
        setReserva(null);
        setReservasCliente([]);
        setMensaje('');

        try {
            const response = await fetch(`http://localhost:8000/reservas/cliente/email/${encodeURIComponent(emailCliente)}`);

            if (response.ok) {
                const data = await response.json();
                setReservasCliente(data);
                if (data.length === 1) {
                    // Si solo hay una reserva, mostrarla directamente
                    setReserva(data[0]);
                }
            } else if (response.status === 404) {
                setError('No se encontraron reservas para ese cliente');
            } else {
                setError('Error al buscar las reservas');
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleBuscarPorTurno = async () => {
        if (!turnoData.id_cancha || !turnoData.id_horario || !turnoData.fecha) {
            setError('Por favor completa todos los campos del turno');
            return;
        }

        setLoading(true);
        setError('');
        setReserva(null);
        setReservasCliente([]);
        setMensaje('');

        try {
            const url = `http://localhost:8000/reservas/turno/buscar?id_cancha=${turnoData.id_cancha}&id_horario=${turnoData.id_horario}&fecha=${turnoData.fecha}`;
            const response = await fetch(url);

            if (response.ok) {
                const data = await response.json();
                setReserva(data);
            } else if (response.status === 404) {
                setError('No se encontró una reserva para ese turno');
            } else {
                setError('Error al buscar la reserva');
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSeleccionarReserva = (reservaSeleccionada) => {
        setReserva(reservaSeleccionada);
        setReservasCliente([]);
    };

    const handleEliminar = () => {
        setShowConfirmDelete(true);
    };

    const handleCancelarEliminar = () => {
        setShowConfirmDelete(false);
    };

    const handleConfirmarEliminar = async () => {
        setLoading(true);
        setMensaje('');
        setError('');
        setShowConfirmDelete(false);

        try {
            const response = await fetch(`http://localhost:8000/reservas/${reserva.id_reserva}`, {
                method: 'DELETE',
            });

            if (response.ok || response.status === 204) {
                setMensaje('Reserva cancelada exitosamente. Los turnos han sido liberados.');
                // Recargar la reserva para mostrar el estado actualizado
                const updatedResponse = await fetch(`http://localhost:8000/reservas/${reserva.id_reserva}/detalles`);
                if (updatedResponse.ok) {
                    const updatedData = await updatedResponse.json();
                    setReserva(updatedData);
                }
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Error al cancelar la reserva');
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleMarcarPagada = () => {
        setShowConfirmPago(true);
    };

    const handleCancelarPago = () => {
        setShowConfirmPago(false);
    };

    const handleConfirmarPago = async () => {
        setLoading(true);
        setMensaje('');
        setError('');
        setShowConfirmPago(false);

        try {
            const response = await fetch(`http://localhost:8000/reservas/${reserva.id_reserva}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    estado_reserva: 'Pagada'
                }),
            });

            if (response.ok) {
                setMensaje('Reserva marcada como pagada exitosamente.');
                // Recargar la reserva para mostrar el estado actualizado
                const updatedResponse = await fetch(`http://localhost:8000/reservas/${reserva.id_reserva}/detalles`);
                if (updatedResponse.ok) {
                    const updatedData = await updatedResponse.json();
                    setReserva(updatedData);
                }
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Error al marcar la reserva como pagada');
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const getEstadoBadgeClass = (estado) => {
        const estadoLower = estado?.toLowerCase() || '';
        if (estadoLower.includes('pagada')) return 'badge-pagada';
        if (estadoLower.includes('pendiente')) return 'badge-pendiente';
        if (estadoLower.includes('cancelada')) return 'badge-cancelada';
        if (estadoLower.includes('finalizada')) return 'badge-finalizada';
        return '';
    };

    return (
        <div className="reservation-manager-overlay">
            <div className="reservation-manager-modal">
                <div className="reservation-manager-header">
                    <h2>Gestión de Reservas</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>

                <div className="reservation-manager-content">
                    {/* Pestañas de búsqueda */}
                    <div className="search-tabs">
                        <button
                            className={`tab ${searchType === 'id' ? 'active' : ''}`}
                            onClick={() => {
                                setSearchType('id');
                                setReserva(null);
                                setReservasCliente([]);
                                setError('');
                                setMensaje('');
                            }}
                        >
                            Por ID
                        </button>
                        <button
                            className={`tab ${searchType === 'email' ? 'active' : ''}`}
                            onClick={() => {
                                setSearchType('email');
                                setReserva(null);
                                setReservasCliente([]);
                                setError('');
                                setMensaje('');
                            }}
                        >
                            Por Cliente
                        </button>
                        <button
                            className={`tab ${searchType === 'turno' ? 'active' : ''}`}
                            onClick={() => {
                                setSearchType('turno');
                                setReserva(null);
                                setReservasCliente([]);
                                setError('');
                                setMensaje('');
                            }}
                        >
                            Por Turno
                        </button>
                    </div>

                    {/* Sección de búsqueda */}
                    <div className="search-section">
                        {searchType === 'id' && (
                            <div className="search-group">
                                <label htmlFor="idReserva">ID de Reserva:</label>
                                <div className="search-input-group">
                                    <input
                                        type="number"
                                        id="idReserva"
                                        value={idReserva}
                                        onChange={(e) => setIdReserva(e.target.value)}
                                        placeholder="Ingresa el ID de la reserva"
                                        disabled={loading}
                                        onKeyPress={(e) => e.key === 'Enter' && handleBuscar()}
                                    />
                                    <button
                                        onClick={handleBuscar}
                                        disabled={loading}
                                        className="search-button"
                                    >
                                        {loading ? 'Buscando...' : 'Buscar'}
                                    </button>
                                </div>
                            </div>
                        )}

                        {searchType === 'email' && (
                            <div className="search-group">
                                <label htmlFor="emailCliente">Email del Cliente:</label>
                                <div className="search-input-group">
                                    <input
                                        type="email"
                                        id="emailCliente"
                                        value={emailCliente}
                                        onChange={(e) => setEmailCliente(e.target.value)}
                                        placeholder="Ingresa el email del cliente"
                                        disabled={loading}
                                        onKeyPress={(e) => e.key === 'Enter' && handleBuscarPorEmail()}
                                    />
                                    <button
                                        onClick={handleBuscarPorEmail}
                                        disabled={loading}
                                        className="search-button"
                                    >
                                        {loading ? 'Buscando...' : 'Buscar'}
                                    </button>
                                </div>
                            </div>
                        )}

                        {searchType === 'turno' && (
                            <div className="search-group-turno">
                                <h4>Buscar por Turno</h4>
                                <div className="turno-fields">
                                    <div className="field-group">
                                        <label htmlFor="id_cancha">ID Cancha:</label>
                                        <input
                                            type="number"
                                            id="id_cancha"
                                            value={turnoData.id_cancha}
                                            onChange={(e) => setTurnoData({ ...turnoData, id_cancha: e.target.value })}
                                            placeholder="ID de la cancha"
                                            disabled={loading}
                                        />
                                    </div>
                                    <div className="field-group">
                                        <label htmlFor="id_horario">ID Horario:</label>
                                        <input
                                            type="number"
                                            id="id_horario"
                                            value={turnoData.id_horario}
                                            onChange={(e) => setTurnoData({ ...turnoData, id_horario: e.target.value })}
                                            placeholder="ID del horario"
                                            disabled={loading}
                                        />
                                    </div>
                                    <div className="field-group">
                                        <label htmlFor="fecha">Fecha:</label>
                                        <input
                                            type="date"
                                            id="fecha"
                                            value={turnoData.fecha}
                                            onChange={(e) => setTurnoData({ ...turnoData, fecha: e.target.value })}
                                            disabled={loading}
                                        />
                                    </div>
                                </div>
                                <button
                                    onClick={handleBuscarPorTurno}
                                    disabled={loading}
                                    className="search-button"
                                >
                                    {loading ? 'Buscando...' : 'Buscar Reserva'}
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Mensajes de error */}
                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}

                    {/* Mensajes de éxito */}
                    {mensaje && (
                        <div className="success-message">
                            {mensaje}
                        </div>
                    )}

                    {/* Lista de reservas del cliente (cuando hay más de una) */}
                    {reservasCliente.length > 1 && (
                        <div className="reservas-list">
                            <h3>Reservas encontradas ({reservasCliente.length})</h3>
                            <div className="reservas-grid">
                                {reservasCliente.map((res) => (
                                    <div
                                        key={res.id_reserva}
                                        className="reserva-card"
                                        onClick={() => handleSeleccionarReserva(res)}
                                    >
                                        <div className="reserva-card-header">
                                            <h4>Reserva #{res.id_reserva}</h4>
                                            <span className={`info-badge ${getEstadoBadgeClass(res.estado_reserva)}`}>
                                                {res.estado_reserva}
                                            </span>
                                        </div>
                                        <div className="reserva-card-body">
                                            <p><strong>Fecha:</strong> {res.fecha_reserva}</p>
                                            <p><strong>Monto:</strong> ${res.monto_total}</p>
                                            <p><strong>Turnos:</strong> {res.detalles?.length || 0}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Información de la reserva */}
                    {reserva && (
                        <div className="reservation-info">
                            <div className="info-header">
                                <h3>Reserva #{reserva.id_reserva}</h3>
                                {reserva.estado_reserva.toLowerCase() === 'pendiente' && (
                                    <div className="action-buttons">
                                        <button onClick={handleMarcarPagada} className="payment-button" disabled={loading}>
                                            ✅ Marcar como Pagada
                                        </button>
                                        <button onClick={handleEliminar} className="delete-button" disabled={loading}>
                                            ❌ Cancelar Reserva
                                        </button>
                                    </div>
                                )}
                            </div>

                            {/* Vista de solo lectura */}
                            <div className="info-grid">
                                <div className="info-item">
                                    <span className="info-label">Cliente ID:</span>
                                    <span className="info-value">{reserva.id_cliente}</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">Fecha de Reserva:</span>
                                    <span className="info-value">{reserva.fecha_reserva}</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">Monto Total:</span>
                                    <span className="info-value">${reserva.monto_total}</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">Estado:</span>
                                    <span className={`info-badge ${getEstadoBadgeClass(reserva.estado_reserva)}`}>
                                        {reserva.estado_reserva}
                                    </span>
                                </div>
                            </div>

                            {/* Mensaje informativo para reservas no pendientes */}
                            {reserva.estado_reserva.toLowerCase() !== 'pendiente' && (
                                <div className="info-message">
                                    <p>ℹ️ Esta reserva está en estado <strong>{reserva.estado_reserva}</strong> y solo puede ser consultada. Las reservas solo pueden eliminarse cuando están en estado <strong>Pendiente</strong>.</p>
                                </div>
                            )}

                            {/* Detalles (turnos) de la reserva */}
                            {reserva.detalles && reserva.detalles.length > 0 && (
                                <div className="reservation-details">
                                    <h4>Turnos Asociados</h4>
                                    <div className="details-table">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>Cancha</th>
                                                    <th>Horario</th>
                                                    <th>Fecha</th>
                                                    <th>Estado Turno</th>
                                                    <th>Precio</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {reserva.detalles.map((detalle, index) => (
                                                    <tr key={index}>
                                                        <td>#{detalle.id_cancha}</td>
                                                        <td>#{detalle.id_horario}</td>
                                                        <td>{detalle.fecha}</td>
                                                        <td>
                                                            <span className={`turno-badge ${detalle.estado_turno.toLowerCase().includes('disponible') ? 'badge-disponible' : 'badge-no-disponible'}`}>
                                                                {detalle.estado_turno}
                                                            </span>
                                                        </td>
                                                        <td>${detalle.precio_total_item}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Modal de confirmación de cancelación */}
                    {showConfirmDelete && (
                        <div className="confirm-modal-overlay">
                            <div className="confirm-modal">
                                <h3>⚠️ Confirmar Cancelación</h3>
                                <p>¿Estás seguro de que deseas cancelar esta reserva?</p>
                                <p className="confirm-details">
                                    Al cancelar esta reserva:
                                </p>
                                <ul className="confirm-list">
                                    <li>La reserva #{reserva.id_reserva} cambiará a estado "Cancelada"</li>
                                    <li>Los turnos asociados ({reserva.detalles?.length || 0} turnos) quedarán disponibles nuevamente</li>
                                    <li>Se conservará el historial de la reserva</li>
                                </ul>
                                <p className="confirm-warning">Solo se pueden cancelar reservas en estado "Pendiente".</p>
                                <div className="confirm-actions">
                                    <button onClick={handleConfirmarEliminar} className="confirm-delete-button" disabled={loading}>
                                        {loading ? 'Cancelando...' : 'Sí, Cancelar Reserva'}
                                    </button>
                                    <button onClick={handleCancelarEliminar} className="confirm-cancel-button" disabled={loading}>
                                        No, Volver
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Modal de confirmación de pago */}
                    {showConfirmPago && (
                        <div className="confirm-modal-overlay">
                            <div className="confirm-modal confirm-modal-payment">
                                <h3>💰 Confirmar Pago</h3>
                                <p>¿Estás seguro de que deseas marcar esta reserva como pagada?</p>
                                <p className="confirm-details">
                                    Al confirmar el pago:
                                </p>
                                <ul className="confirm-list confirm-list-payment">
                                    <li>La reserva #{reserva.id_reserva} cambiará a estado "Pagada"</li>
                                    <li>Los turnos asociados ({reserva.detalles?.length || 0} turnos) quedarán confirmados</li>
                                    <li>El monto total es: ${reserva.monto_total}</li>
                                </ul>
                                <p className="confirm-warning confirm-warning-payment">Esta acción confirma que se recibió el pago del cliente.</p>
                                <div className="confirm-actions">
                                    <button onClick={handleConfirmarPago} className="confirm-payment-button" disabled={loading}>
                                        {loading ? 'Procesando...' : 'Sí, Confirmar Pago'}
                                    </button>
                                    <button onClick={handleCancelarPago} className="confirm-cancel-button" disabled={loading}>
                                        No, Volver
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ReservationManager;
