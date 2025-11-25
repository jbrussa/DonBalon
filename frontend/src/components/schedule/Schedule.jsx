import React, { useEffect, useMemo, useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import Login from "../auth/Login";
import Payment from "../payment/Payment";
import "./Schedule.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function isoDate(d) {
  return d.toISOString().slice(0, 10);
}

export default function Schedule() {
  const [canchas, setCanchas] = useState([]);
  const [horarios, setHorarios] = useState([]);
  const [turnos, setTurnos] = useState([]);
  const [canchaServicios, setCanchaServicios] = useState([]);
  const [servicios, setServicios] = useState([]);
  const [date, setDate] = useState(isoDate(new Date()));
  const [hoverSlot, setHoverSlot] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);
  const [selectedTurnos, setSelectedTurnos] = useState([]);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [loginMessage, setLoginMessage] = useState("");
  const { isAuthenticated } = useAuth();

  // Inicializar turnos al cargar el componente
  useEffect(() => {
    async function inicializarTurnos() {
      try {
        // Primero expirar turnos pasados
        await fetch(`${API_BASE}/turnos/expirar-pasados`, {
          method: 'POST',
        });

        // Luego crear turnos del día actual si no existen
        await fetch(`${API_BASE}/turnos/crear-del-dia`, {
          method: 'POST',
        });

        console.log('Turnos inicializados correctamente');
      } catch (error) {
        console.error('Error al inicializar turnos:', error);
      } finally {
        setIsInitializing(false);
      }
    }

    inicializarTurnos();
  }, []);

  useEffect(() => {
    // Esperar a que la inicialización termine antes de cargar datos
    if (isInitializing) return;

    fetch(`${API_BASE}/canchas`)
      .then((r) => r.json())
      .then(setCanchas)
      .catch(() => setCanchas([]));
    fetch(`${API_BASE}/horarios`)
      .then((r) => r.json())
      .then(setHorarios)
      .catch(() => setHorarios([]));
    fetch(`${API_BASE}/turnos`)
      .then((r) => r.json())
      .then(setTurnos)
      .catch(() => setTurnos([]));
    fetch(`${API_BASE}/canchas-servicios`)
      .then((r) => r.json())
      .then(setCanchaServicios)
      .catch(() => setCanchaServicios([]));
    fetch(`${API_BASE}/servicios`)
      .then((r) => r.json())
      .then(setServicios)
      .catch(() => setServicios([]));
  }, [isInitializing]);

  // Crear turnos cuando cambia la fecha seleccionada
  useEffect(() => {
    if (isInitializing || !date) return;

    async function crearTurnosFecha() {
      try {
        await fetch(`${API_BASE}/turnos/crear-del-dia?fecha=${date}`, {
          method: 'POST',
        });

        // Recargar los turnos después de crearlos
        const turnosResponse = await fetch(`${API_BASE}/turnos`);
        const turnosData = await turnosResponse.json();
        setTurnos(turnosData);
      } catch (error) {
        console.error('Error al crear turnos para la fecha seleccionada:', error);
      }
    }

    crearTurnosFecha();
  }, [date, isInitializing]);

  // Map horarios to sorted time slots (use hora_inicio)
  const timeSlots = useMemo(() => {
    if (!horarios || horarios.length === 0) {
      // default 8..22 hourly slots
      return Array.from({ length: 14 }).map((_, i) => ({
        label: `${8 + i}:00`,
        id: `slot-${8 + i}`,
        hour: 8 + i,
      }));
    }
    // Convert horario objects: expect {id_horario, hora_inicio, hora_fin}
    const parsed = horarios.map((h) => {
      let start = h.hora_inicio || h.horaInicio || h.hora_inicio || "";
      const hour = parseInt(start.split(":")[0], 10);
      return { id: h.id_horario ?? h.id, label: start.slice(0, 5), hour };
    });
    parsed.sort((a, b) => a.hour - b.hour);
    return parsed;
  }, [horarios]);

  // build map of turnos for selected date (both available and unavailable)
  const turnosMap = useMemo(() => {
    const map = {};
    turnos.forEach((t) => {
      if (!t.fecha) return;
      if (t.fecha !== date) return;
      const canchaId = t.id_cancha ?? t.idCancha ?? t["id_cancha"];
      const horarioId = t.id_horario ?? t.idHorario ?? t["id_horario"];
      // find horario to get hour
      const h = horarios.find((x) => (x.id_horario ?? x.id) === horarioId);
      let hour = null;
      if (h && h.hora_inicio) hour = parseInt(h.hora_inicio.split(":")[0], 10);
      if (hour === null && t.hora_inicio)
        hour = parseInt(t.hora_inicio.split(":")[0], 10);
      if (hour === null) return;
      const key = `${canchaId}__${hour}`;
      map[key] = t;
    });
    return map;
  }, [turnos, horarios, date]);

  // services per cancha
  const servicesByCancha = useMemo(() => {
    const map = {};
    canchaServicios.forEach((cs) => {
      const id = cs.id_cancha ?? cs.idCancha ?? cs.id_cancha;
      if (!map[id]) map[id] = [];
      const svc = servicios.find(
        (s) => s.id_servicio === cs.id_servicio || s.id === cs.id_servicio
      );
      if (svc) map[id].push(svc);
    });
    return map;
  }, [canchaServicios, servicios]);

  // Función para verificar si un turno está seleccionado
  const isTurnoSelected = (turnoId) => {
    return selectedTurnos.some(t => t.id_turno === turnoId);
  };

  // Función para alternar la selección de un turno
  const toggleTurnoSelection = (turno, cancha, horario) => {
    const turnoId = turno.id_turno;

    if (isTurnoSelected(turnoId)) {
      // Deseleccionar
      setSelectedTurnos(prev => prev.filter(t => t.id_turno !== turnoId));
    } else {
      // Seleccionar - guardar el turno con información adicional
      setSelectedTurnos(prev => [
        ...prev,
        {
          ...turno,
          cancha_nombre: cancha.nombre,
          horario_inicio: horario.label,
        }
      ]);
    }
  };

  // Función para limpiar todas las selecciones
  const clearSelection = () => {
    setSelectedTurnos([]);
  };

  // Función para proceder con la reserva
  const handleProcederReserva = () => {
    if (selectedTurnos.length === 0) {
      alert('Debe seleccionar al menos un turno');
      return;
    }

    // Validar que ningún turno sea de una fecha pasada
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);

    const turnosPasados = selectedTurnos.filter(turno => {
      const fechaTurno = new Date(turno.fecha + 'T00:00:00');
      return fechaTurno < hoy;
    });

    if (turnosPasados.length > 0) {
      alert('No se pueden reservar turnos de fechas pasadas. Por favor, seleccione solo turnos de fechas actuales o futuras.');
      // Limpiar los turnos pasados de la selección
      setSelectedTurnos(selectedTurnos.filter(t => !turnosPasados.includes(t)));
      return;
    }

    // Verificar si hay sesión iniciada
    if (!isAuthenticated()) {
      setLoginMessage("Debes iniciar sesión para continuar con la reserva");
      setShowLoginModal(true);
      return;
    }

    // Si hay sesión, abrir modal de pago
    setShowPaymentModal(true);
  };

  // Callback cuando se cierra el modal de login
  const handleCloseLogin = () => {
    setShowLoginModal(false);
    setLoginMessage("");

    // Si después de cerrar el login el usuario se autenticó, abrir modal de pago
    if (isAuthenticated() && selectedTurnos.length > 0) {
      setShowPaymentModal(true);
    }
  };

  // Callback cuando se cierra el modal de pago
  const handleClosePayment = () => {
    setShowPaymentModal(false);
    // Limpiar selecciones y recargar datos
    setSelectedTurnos([]);

    // Recargar turnos para actualizar disponibilidad
    fetch(`${API_BASE}/turnos`)
      .then((r) => r.json())
      .then(setTurnos)
      .catch(() => setTurnos([]));
  };

  function renderRow(cancha) {
    const cid = cancha.id_cancha ?? cancha.id;
    // build array of cells: left + one cell per timeSlot
    const cells = [];
    // left cell
    cells.push(
      <div className="schedule-left" key={`left-${cid}`}>
        <div className="cancha-name">{cancha.nombre}</div>
        <div className="cancha-meta">
          {(servicesByCancha[cid] || []).map((s) => s.descripcion).join(" · ")}
        </div>
      </div>
    );

    // time slot cells as direct children so grid columns align
    timeSlots.forEach((slot) => {
      const key = `${cid}__${slot.hour}`;
      const turno = turnosMap[key];

      // Determinar disponibilidad según el estado del turno
      let slotClass = "slot";
      let isClickable = false;
      let tooltipText = "";
      let isSelected = false;

      if (!turno) {
        // No existe turno para este slot - No disponible (no creado)
        slotClass += " no-turno";
        tooltipText = "No hay turno creado para este horario";
      } else {
        const estadoTurno = (turno.estado_turno || "").toLowerCase();
        if (estadoTurno === "disponible") {
          isSelected = isTurnoSelected(turno.id_turno);
          slotClass += " available";
          if (isSelected) {
            slotClass += " selected";
          }
          isClickable = true;
          tooltipText = isSelected ? "Click para deseleccionar" : "Click para seleccionar";
        } else {
          // "no disponible" o cualquier otro estado
          slotClass += " occupied";
          tooltipText = "No disponible";
        }
      }

      cells.push(
        <div
          key={slot.id + key}
          className={slotClass}
          onMouseEnter={() => setHoverSlot(isClickable && !isSelected ? key : null)}
          onMouseLeave={() => setHoverSlot(null)}
          onClick={() => {
            if (isClickable) {
              toggleTurnoSelection(turno, cancha, slot);
            }
          }}
          title={tooltipText}
        >
          {isSelected ? (
            <div className="slot-selected-indicator" />
          ) : hoverSlot === key && isClickable ? (
            <div className="slot-hover" />
          ) : null}
        </div>
      );
    });

    const template = `220px repeat(${timeSlots.length}, 1fr)`;

    return (
      <div
        className="schedule-row"
        key={cid}
        style={{ gridTemplateColumns: template }}
      >
        {cells}
      </div>
    );
  }

  const template = `220px repeat(${timeSlots.length}, 1fr)`;

  if (isInitializing) {
    return (
      <div className="schedule-root">
        <div className="schedule-loading">
          <p>Inicializando turnos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="schedule-root">
      <div className="schedule-controls">
        <label>
          Fecha:{" "}
          <input
            type="date"
            value={date}
            min={isoDate(new Date())}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
        <div className="legend">
          <div className="legend-item">
            <span className="legend-swatch selected" /> Seleccionado
          </div>
          <div className="legend-item">
            <span className="legend-swatch occupied" /> No disponible
          </div>
          <div className="legend-item">
            <span className="legend-swatch available" /> Disponible
          </div>
        </div>
      </div>

      <div className="schedule-grid">
        <div
          className="schedule-header"
          style={{ gridTemplateColumns: template }}
        >
          <div className="schedule-left header-left">Cancha</div>
          {timeSlots.map((s) => (
            <div key={s.id} className="slot header-slot">
              {s.label}
            </div>
          ))}
        </div>

        <div className="schedule-body">{canchas.map(renderRow)}</div>
      </div>

      {/* Sección de turnos seleccionados y botón de reserva */}
      {selectedTurnos.length > 0 && (
        <div className="reservation-section">
          <div className="selected-turnos-summary">
            <h3>Turnos seleccionados ({selectedTurnos.length})</h3>
            <div className="selected-turnos-list">
              {selectedTurnos.map((turno) => (
                <div key={turno.id_turno} className="selected-turno-item">
                  <div className="turno-info">
                    <span className="turno-cancha">{turno.cancha_nombre}</span>
                    <span className="turno-horario">{turno.horario_inicio}</span>
                    <span className="turno-fecha">{turno.fecha}</span>
                  </div>
                  <button
                    className="remove-turno-btn"
                    onClick={() => toggleTurnoSelection(turno, { nombre: turno.cancha_nombre }, { label: turno.horario_inicio })}
                    title="Quitar turno"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="reservation-actions">
            <button className="clear-selection-btn" onClick={clearSelection}>
              Limpiar selección
            </button>
            <button className="proceed-reservation-btn" onClick={handleProcederReserva}>
              Proceder con la reserva
            </button>
          </div>
        </div>
      )}

      {/* Modal de login si no está autenticado */}
      {showLoginModal && <Login onClose={handleCloseLogin} message={loginMessage} />}

      {/* Modal de pago */}
      {showPaymentModal && (
        <Payment
          selectedTurnos={selectedTurnos}
          onClose={handleClosePayment}
        />
      )}
    </div>
  );
}
