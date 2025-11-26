import React, { useState } from 'react';
import './UserManager.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function UserManager({ onClose }) {
    const [email, setEmail] = useState('');
    const [usuario, setUsuario] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [editando, setEditando] = useState(false);
    const [mensaje, setMensaje] = useState('');

    // Datos del formulario de edición
    const [formData, setFormData] = useState({
        nombre: '',
        apellido: '',
        telefono: '',
        mail: '',
        password: '',
        admin: false
    });

    const handleBuscar = async () => {
        if (!email.trim()) {
            setError('Debe ingresar un email');
            return;
        }

        setError('');
        setMensaje('');
        setLoading(true);
        setUsuario(null);
        setEditando(false);

        try {
            const response = await fetch(`${API_BASE}/clientes/email/${encodeURIComponent(email)}`);

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Usuario no encontrado');
                }
                throw new Error('Error al buscar usuario');
            }

            const data = await response.json();
            setUsuario(data);
            setFormData({
                nombre: data.nombre,
                apellido: data.apellido,
                telefono: data.telefono,
                mail: data.mail,
                password: data.password,
                admin: data.admin
            });
        } catch (err) {
            setError(err.message || 'Error al buscar usuario');
        } finally {
            setLoading(false);
        }
    };

    const handleEditar = () => {
        setEditando(true);
        setMensaje('');
        setError('');
    };

    const handleCancelarEdicion = () => {
        setEditando(false);
        // Restaurar datos originales
        setFormData({
            nombre: usuario.nombre,
            apellido: usuario.apellido,
            telefono: usuario.telefono,
            mail: usuario.mail,
            password: usuario.password,
            admin: usuario.admin
        });
        setError('');
        setMensaje('');
    };

    const handleGuardar = async () => {
        setError('');
        setMensaje('');

        // Validaciones
        if (!formData.nombre.trim()) {
            setError('El nombre es obligatorio');
            return;
        }
        if (!formData.apellido.trim()) {
            setError('El apellido es obligatorio');
            return;
        }
        if (!formData.mail.trim()) {
            setError('El email es obligatorio');
            return;
        }
        if (!formData.telefono.trim()) {
            setError('El teléfono es obligatorio');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(`${API_BASE}/clientes/${usuario.id_cliente}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al actualizar usuario');
            }

            const usuarioActualizado = await response.json();
            setUsuario(usuarioActualizado);
            setFormData({
                nombre: usuarioActualizado.nombre,
                apellido: usuarioActualizado.apellido,
                telefono: usuarioActualizado.telefono,
                mail: usuarioActualizado.mail,
                password: usuarioActualizado.password,
                admin: usuarioActualizado.admin
            });
            setEditando(false);
            setMensaje('Usuario actualizado exitosamente');
        } catch (err) {
            setError(err.message || 'Error al actualizar usuario');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    return (
        <div className="user-manager-overlay" onClick={onClose}>
            <div className="user-manager-modal" onClick={(e) => e.stopPropagation()}>
                <button className="user-manager-close" onClick={onClose}>✕</button>

                <div className="user-manager-content">
                    <h2>Gestión de Usuarios</h2>
                    <p className="user-manager-description">
                        Busque un usuario por email para ver y actualizar su información
                    </p>

                    {/* Búsqueda */}
                    <div className="search-section">
                        <div className="search-field">
                            <label>Email del Usuario</label>
                            <div className="search-input-group">
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="usuario@ejemplo.com"
                                    onKeyPress={(e) => e.key === 'Enter' && handleBuscar()}
                                />
                                <button
                                    onClick={handleBuscar}
                                    className="btn-search"
                                    disabled={loading}
                                >
                                    {loading ? 'Buscando...' : 'Buscar'}
                                </button>
                            </div>
                        </div>
                    </div>

                    {error && <div className="user-manager-error">{error}</div>}
                    {mensaje && <div className="user-manager-success">{mensaje}</div>}

                    {/* Información del usuario */}
                    {usuario && (
                        <div className="user-info-section">
                            <div className="user-info-header">
                                <h3>Información del Usuario</h3>
                                {!editando && (
                                    <button onClick={handleEditar} className="btn-edit">
                                        Editar
                                    </button>
                                )}
                            </div>

                            <div className="user-form">
                                <div className="form-row">
                                    <div className="form-field">
                                        <label>ID de Cliente</label>
                                        <input
                                            type="text"
                                            value={usuario.id_cliente}
                                            disabled
                                        />
                                    </div>
                                    <div className="form-field">
                                        <label>Nombre</label>
                                        <input
                                            type="text"
                                            name="nombre"
                                            value={formData.nombre}
                                            onChange={handleInputChange}
                                            disabled={!editando}
                                        />
                                    </div>
                                </div>

                                <div className="form-row">
                                    <div className="form-field">
                                        <label>Apellido</label>
                                        <input
                                            type="text"
                                            name="apellido"
                                            value={formData.apellido}
                                            onChange={handleInputChange}
                                            disabled={!editando}
                                        />
                                    </div>
                                    <div className="form-field">
                                        <label>Teléfono</label>
                                        <input
                                            type="tel"
                                            name="telefono"
                                            value={formData.telefono}
                                            onChange={(e) => {
                                                // Solo permitir números
                                                const value = e.target.value.replace(/\D/g, '');
                                                handleInputChange({ target: { name: 'telefono', value } });
                                            }}
                                            disabled={!editando}
                                        />
                                    </div>
                                </div>

                                <div className="form-field">
                                    <label>Email</label>
                                    <input
                                        type="email"
                                        name="mail"
                                        value={formData.mail}
                                        onChange={handleInputChange}
                                        disabled={!editando}
                                    />
                                </div>

                                <div className="form-field">
                                    <label>Contraseña</label>
                                    <input
                                        type="text"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        disabled={!editando}
                                        placeholder="Dejar en blanco para no cambiar"
                                    />
                                    {!editando && (
                                        <small>La contraseña está protegida</small>
                                    )}
                                </div>

                                <div className="form-field-checkbox">
                                    <label className="checkbox-label">
                                        <input
                                            type="checkbox"
                                            name="admin"
                                            checked={formData.admin}
                                            onChange={handleInputChange}
                                            disabled={!editando}
                                        />
                                        <span>Usuario Administrador</span>
                                    </label>
                                    <small>Los administradores tienen acceso a reportes y gestión de usuarios</small>
                                </div>

                                {editando && (
                                    <div className="form-actions">
                                        <button
                                            onClick={handleCancelarEdicion}
                                            className="btn-cancel"
                                            disabled={loading}
                                        >
                                            Cancelar
                                        </button>
                                        <button
                                            onClick={handleGuardar}
                                            className="btn-save"
                                            disabled={loading}
                                        >
                                            {loading ? 'Guardando...' : 'Guardar Cambios'}
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
