import React, { useState, useEffect } from 'react';
import './FieldManager.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function FieldManager({ onClose }) {
    const [canchas, setCanchas] = useState([]);
    const [tiposCancha, setTiposCancha] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [modoEdicion, setModoEdicion] = useState(false);
    const [modoCreacion, setModoCreacion] = useState(false);
    const [canchaSeleccionada, setCanchaSeleccionada] = useState(null);

    const [formData, setFormData] = useState({
        nombre: '',
        id_tipo: ''
    });

    // Cargar canchas y tipos al montar el componente
    useEffect(() => {
        cargarCanchas();
        cargarTiposCancha();
    }, []);

    const cargarCanchas = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetch(`${API_BASE}/canchas/`);
            if (!response.ok) throw new Error('Error al cargar canchas');
            const data = await response.json();
            setCanchas(data);
        } catch (err) {
            setError(err.message || 'Error al cargar canchas');
        } finally {
            setLoading(false);
        }
    };

    const cargarTiposCancha = async () => {
        try {
            const response = await fetch(`${API_BASE}/tipos-cancha/`);
            if (!response.ok) throw new Error('Error al cargar tipos de cancha');
            const data = await response.json();
            setTiposCancha(data);
        } catch (err) {
            console.error('Error al cargar tipos:', err);
        }
    };

    const handleNuevaCancha = () => {
        setModoCreacion(true);
        setModoEdicion(false);
        setCanchaSeleccionada(null);
        setFormData({
            nombre: '',
            id_tipo: tiposCancha.length > 0 ? tiposCancha[0].id_tipo : ''
        });
        setError('');
        setMensaje('');
    };

    const handleEditarCancha = (cancha) => {
        setModoEdicion(true);
        setModoCreacion(false);
        setCanchaSeleccionada(cancha);
        setFormData({
            nombre: cancha.nombre,
            id_tipo: cancha.id_tipo
        });
        setError('');
        setMensaje('');
    };

    const handleCancelar = () => {
        setModoEdicion(false);
        setModoCreacion(false);
        setCanchaSeleccionada(null);
        setFormData({ nombre: '', id_tipo: '' });
        setError('');
        setMensaje('');
    };

    const handleCrear = async () => {
        if (!formData.nombre.trim()) {
            setError('El nombre de la cancha es obligatorio');
            return;
        }
        if (!formData.id_tipo) {
            setError('Debe seleccionar un tipo de cancha');
            return;
        }

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/canchas/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: formData.nombre,
                    id_tipo: parseInt(formData.id_tipo)
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al crear cancha');
            }

            setMensaje('Cancha creada exitosamente');
            await cargarCanchas();
            handleCancelar();
        } catch (err) {
            setError(err.message || 'Error al crear cancha');
        } finally {
            setLoading(false);
        }
    };

    const handleGuardar = async () => {
        if (!formData.nombre.trim()) {
            setError('El nombre de la cancha es obligatorio');
            return;
        }
        if (!formData.id_tipo) {
            setError('Debe seleccionar un tipo de cancha');
            return;
        }

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/canchas/${canchaSeleccionada.id_cancha}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: formData.nombre,
                    id_tipo: parseInt(formData.id_tipo)
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al actualizar cancha');
            }

            setMensaje('Cancha actualizada exitosamente');
            await cargarCanchas();
            handleCancelar();
        } catch (err) {
            setError(err.message || 'Error al actualizar cancha');
        } finally {
            setLoading(false);
        }
    };

    const handleEliminar = async (cancha) => {
        if (!window.confirm(`¿Está seguro de desactivar la cancha "${cancha.nombre}"?\n\nLa cancha se marcará como inactiva pero se conservarán todos los registros históricos de reservas y turnos asociados.`)) {
            return;
        }

        setLoading(true);
        setError('');
        setMensaje('');

        try {
            const response = await fetch(`${API_BASE}/canchas/${cancha.id_cancha}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Error al desactivar cancha');
            }

            setMensaje('Cancha desactivada exitosamente. Los datos históricos se han conservado.');
            await cargarCanchas();
        } catch (err) {
            setError(err.message || 'Error al desactivar cancha');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const getTipoNombre = (id_tipo) => {
        const tipo = tiposCancha.find(t => t.id_tipo === id_tipo);
        return tipo ? tipo.descripcion : 'N/A';
    };

    return (
        <div className="field-manager-overlay" onClick={onClose}>
            <div className="field-manager-modal" onClick={(e) => e.stopPropagation()}>
                <div className="field-manager-header">
                    <h2>Gestión de Canchas</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>

                <div className="field-manager-content">
                    {error && <div className="error-message">{error}</div>}
                    {mensaje && <div className="success-message">{mensaje}</div>}

                    {!modoEdicion && !modoCreacion && (
                        <>
                            <div className="action-bar">
                                <button
                                    className="new-button"
                                    onClick={handleNuevaCancha}
                                    disabled={loading}
                                >
                                    + Nueva Cancha
                                </button>
                            </div>

                            <div className="list-section">
                                <h3>Canchas Registradas ({canchas.length})</h3>
                                {loading ? (
                                    <p className="loading-text">Cargando...</p>
                                ) : canchas.length === 0 ? (
                                    <p className="empty-text">No hay canchas registradas</p>
                                ) : (
                                    <div className="items-grid">
                                        {canchas.map(cancha => (
                                            <div key={cancha.id_cancha} className="item-card">
                                                <div className="item-card-header">
                                                    <h4>{cancha.nombre}</h4>
                                                </div>
                                                <div className="item-card-body">
                                                    <p><strong>Tipo:</strong> {getTipoNombre(cancha.id_tipo)}</p>
                                                    <p><strong>ID:</strong> {cancha.id_cancha}</p>
                                                </div>
                                                <div className="item-card-actions">
                                                    <button
                                                        className="edit-button-small"
                                                        onClick={() => handleEditarCancha(cancha)}
                                                        disabled={loading}
                                                    >
                                                        Editar
                                                    </button>
                                                    <button
                                                        className="delete-button-small"
                                                        onClick={() => handleEliminar(cancha)}
                                                        disabled={loading}
                                                    >
                                                        Desactivar
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </>
                    )}

                    {(modoCreacion || modoEdicion) && (
                        <div className="form-section">
                            <h3>{modoCreacion ? 'Crear Nueva Cancha' : 'Editar Cancha'}</h3>

                            <div className="form-group">
                                <label>Nombre de la Cancha *</label>
                                <input
                                    type="text"
                                    name="nombre"
                                    value={formData.nombre}
                                    onChange={handleInputChange}
                                    placeholder="Ej: Cancha 1"
                                    disabled={loading}
                                />
                            </div>

                            <div className="form-group">
                                <label>Tipo de Cancha *</label>
                                <select
                                    name="id_tipo"
                                    value={formData.id_tipo}
                                    onChange={handleInputChange}
                                    disabled={loading}
                                >
                                    <option value="">Seleccione un tipo</option>
                                    {tiposCancha.map(tipo => (
                                        <option key={tipo.id_tipo} value={tipo.id_tipo}>
                                            {tipo.descripcion} - ${tipo.precio_hora}/hora
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-actions">
                                <button
                                    className="save-button"
                                    onClick={modoCreacion ? handleCrear : handleGuardar}
                                    disabled={loading}
                                >
                                    {loading ? 'Guardando...' : (modoCreacion ? 'Crear' : 'Guardar')}
                                </button>
                                <button
                                    className="cancel-button"
                                    onClick={handleCancelar}
                                    disabled={loading}
                                >
                                    Cancelar
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
