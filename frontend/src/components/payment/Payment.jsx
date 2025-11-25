import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import ReservationConfirmation from './ReservationConfirmation';
import './Payment.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Payment = ({ selectedTurnos, onClose }) => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [processingPayment, setProcessingPayment] = useState(false);
    const [error, setError] = useState('');
    const [canchasDetalle, setCanchasDetalle] = useState([]);
    const [metodoPago, setMetodoPago] = useState('');
    const [metodosPago, setMetodosPago] = useState([]);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [reservaId, setReservaId] = useState(null);

    // Campos de tarjeta
    const [numeroTarjeta, setNumeroTarjeta] = useState('');
    const [fechaVencimiento, setFechaVencimiento] = useState('');
    const [codigoSeguridad, setCodigoSeguridad] = useState('');

    // Cargar métodos de pago y detalles de canchas
    useEffect(() => {
        const cargarDatos = async () => {
            try {
                setLoading(true);

                // Obtener métodos de pago
                const metodosRes = await fetch(`${API_BASE}/metodos-pago`);
                const metodosData = await metodosRes.json();
                setMetodosPago(metodosData);

                // Obtener detalles de cada cancha seleccionada
                const canchasIds = [...new Set(selectedTurnos.map(t => t.id_cancha))];
                const detallesPromises = canchasIds.map(id =>
                    fetch(`${API_BASE}/canchas-servicios/cancha/${id}/detalle`).then(r => r.json())
                );

                const detalles = await Promise.all(detallesPromises);
                setCanchasDetalle(detalles);

            } catch (err) {
                console.error('Error al cargar datos:', err);
                setError('Error al cargar información de pago');
            } finally {
                setLoading(false);
            }
        };

        cargarDatos();
    }, [selectedTurnos]);

    // Calcular totales
    const calcularTotales = () => {
        const totalesPorCancha = {};

        selectedTurnos.forEach(turno => {
            const cancha = canchasDetalle.find(c => c.id_cancha === turno.id_cancha);
            if (cancha) {
                if (!totalesPorCancha[turno.id_cancha]) {
                    totalesPorCancha[turno.id_cancha] = {
                        nombre: cancha.nombre,
                        precio_hora: parseFloat(cancha.precio_hora),
                        precio_total: parseFloat(cancha.precio_total),
                        servicios: cancha.servicios,
                        cantidad: 0,
                        subtotal: 0
                    };
                }
                totalesPorCancha[turno.id_cancha].cantidad++;
                totalesPorCancha[turno.id_cancha].subtotal += parseFloat(cancha.precio_total);
            }
        });

        const total = Object.values(totalesPorCancha).reduce((sum, item) => sum + item.subtotal, 0);

        return { totalesPorCancha, total };
    };

    const { totalesPorCancha, total } = calcularTotales();

    // Validar campos de tarjeta
    const validarCamposTarjeta = () => {
        if (!numeroTarjeta || numeroTarjeta.replace(/\s/g, '').length < 13) {
            setError('Número de tarjeta inválido');
            return false;
        }

        // Validar formato MM/AAAA
        const fechaRegex = /^(0[1-9]|1[0-2])\/\d{4}$/;
        if (!fechaVencimiento || !fechaRegex.test(fechaVencimiento)) {
            setError('Fecha de vencimiento inválida (formato: MM/AAAA)');
            return false;
        }

        if (!codigoSeguridad || codigoSeguridad.length < 3) {
            setError('Código de seguridad inválido');
            return false;
        }

        return true;
    };

    // Procesar pago
    const handlePagar = async () => {
        setError('');

        if (!metodoPago) {
            setError('Debe seleccionar un método de pago');
            return;
        }

        // Si es tarjeta, validar campos
        const metodoSeleccionado = metodosPago.find(m => m.id_metodo_pago.toString() === metodoPago);
        if (metodoSeleccionado && metodoSeleccionado.descripcion.toLowerCase().includes('tarjeta')) {
            if (!validarCamposTarjeta()) {
                return;
            }
        }

        setProcessingPayment(true);

        try {
            // Preparar datos de la reserva
            const reservaData = {
                id_cliente: user.id_cliente,
                id_metodo_pago: parseInt(metodoPago),
                items: selectedTurnos.map(turno => ({
                    id_cancha: turno.id_cancha,
                    id_horario: turno.id_horario,
                    fecha: turno.fecha
                }))
            };

            // Crear la reserva
            const response = await fetch(`${API_BASE}/reservas/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reservaData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al procesar la reserva');
            }

            const reservaCreada = await response.json();

            // Mostrar confirmación
            setReservaId(reservaCreada.id_reserva);
            setShowConfirmation(true);

        } catch (err) {
            console.error('Error al procesar pago:', err);
            setError(err.message || 'Error al procesar el pago. Por favor intente nuevamente.');
        } finally {
            setProcessingPayment(false);
        }
    };

    // Formatear número de tarjeta con espacios
    const formatearNumeroTarjeta = (valor) => {
        const limpio = valor.replace(/\s/g, '');
        const grupos = limpio.match(/.{1,4}/g);
        return grupos ? grupos.join(' ') : limpio;
    };

    const handleNumeroTarjetaChange = (e) => {
        const valor = e.target.value.replace(/\D/g, '').slice(0, 16);
        setNumeroTarjeta(formatearNumeroTarjeta(valor));
    };

    const handleFechaVencimientoChange = (e) => {
        let valor = e.target.value.replace(/\D/g, '');
        if (valor.length >= 2) {
            valor = valor.slice(0, 2) + '/' + valor.slice(2, 6);
        }
        setFechaVencimiento(valor);
    };

    const handleCodigoSeguridadChange = (e) => {
        const valor = e.target.value.replace(/\D/g, '').slice(0, 4);
        setCodigoSeguridad(valor);
    };

    if (showConfirmation) {
        return (
            <ReservationConfirmation
                reservaId={reservaId}
                onClose={onClose}
            />
        );
    }

    if (loading) {
        return (
            <div className="payment-overlay">
                <div className="payment-modal">
                    <div className="payment-loading">
                        <p>Cargando información...</p>
                    </div>
                </div>
            </div>
        );
    }

    const mostrarCamposTarjeta = metodosPago.find(m => m.id_metodo_pago.toString() === metodoPago)?.descripcion.toLowerCase().includes('tarjeta');

    return (
        <div className="payment-overlay" onClick={onClose}>
            <div className="payment-modal" onClick={(e) => e.stopPropagation()}>
                <button className="payment-close" onClick={onClose}>×</button>

                <h2 className="payment-title">Resumen de Reserva</h2>

                {error && (
                    <div className="payment-error">
                        {error}
                    </div>
                )}

                {/* Resumen de canchas seleccionadas */}
                <div className="payment-section">
                    <h3>Canchas Seleccionadas</h3>
                    {Object.entries(totalesPorCancha).map(([idCancha, info]) => (
                        <div key={idCancha} className="cancha-item">
                            <div className="cancha-header">
                                <h4>{info.nombre}</h4>
                                <span className="cancha-cantidad">{info.cantidad} turno(s)</span>
                            </div>

                            {info.servicios && info.servicios.length > 0 && (
                                <div className="cancha-servicios">
                                    <strong>Servicios disponibles:</strong>
                                    <ul>
                                        {info.servicios.map(servicio => (
                                            <li key={servicio.id_servicio}>
                                                {servicio.descripcion}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            <div className="cancha-precio">
                                <span>Precio por turno: ${info.precio_total.toFixed(2)}</span>
                                <span className="subtotal">Subtotal: ${info.subtotal.toFixed(2)}</span>
                            </div>
                        </div>
                    ))}

                    <div className="payment-total">
                        <strong>Total a Pagar:</strong>
                        <span className="total-amount">${total.toFixed(2)}</span>
                    </div>
                </div>

                {/* Selección de método de pago */}
                <div className="payment-section">
                    <h3>Método de Pago</h3>
                    <div className="payment-methods">
                        {metodosPago.map(metodo => (
                            <label key={metodo.id_metodo_pago} className="payment-method-option">
                                <input
                                    type="radio"
                                    name="metodoPago"
                                    value={metodo.id_metodo_pago}
                                    checked={metodoPago === metodo.id_metodo_pago.toString()}
                                    onChange={(e) => setMetodoPago(e.target.value)}
                                    disabled={processingPayment}
                                />
                                <span>{metodo.descripcion}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Campos de tarjeta (si se selecciona tarjeta) */}
                {mostrarCamposTarjeta && (
                    <div className="payment-section">
                        <h3>Datos de la Tarjeta</h3>
                        <div className="card-fields">
                            <div className="payment-field">
                                <label htmlFor="numeroTarjeta">Número de Tarjeta *</label>
                                <input
                                    type="text"
                                    id="numeroTarjeta"
                                    value={numeroTarjeta}
                                    onChange={handleNumeroTarjetaChange}
                                    placeholder="1234 5678 9012 3456"
                                    maxLength="19"
                                    required
                                    disabled={processingPayment}
                                />
                            </div>

                            <div className="card-row">
                                <div className="payment-field">
                                    <label htmlFor="fechaVencimiento">Vencimiento (MM/AAAA) *</label>
                                    <input
                                        type="text"
                                        id="fechaVencimiento"
                                        value={fechaVencimiento}
                                        onChange={handleFechaVencimientoChange}
                                        placeholder="12/2025"
                                        maxLength="7"
                                        required
                                        disabled={processingPayment}
                                    />
                                </div>

                                <div className="payment-field">
                                    <label htmlFor="codigoSeguridad">CVV *</label>
                                    <input
                                        type="text"
                                        id="codigoSeguridad"
                                        value={codigoSeguridad}
                                        onChange={handleCodigoSeguridadChange}
                                        placeholder="123"
                                        maxLength="4"
                                        required
                                        disabled={processingPayment}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Botón de pago */}
                <button
                    className="payment-submit"
                    onClick={handlePagar}
                    disabled={processingPayment || !metodoPago}
                >
                    {processingPayment ? 'Procesando...' : 'Pagar'}
                </button>
            </div>
        </div>
    );
};

export default Payment;
