import React, { useEffect, useMemo, useState } from "react";
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

      if (!turno) {
        // No existe turno para este slot - No disponible (no creado)
        slotClass += " no-turno";
        tooltipText = "No hay turno creado para este horario";
      } else {
        const estadoTurno = (turno.estado_turno || "").toLowerCase();
        if (estadoTurno === "disponible") {
          slotClass += " available";
          isClickable = true;
          tooltipText = "Haz click para reservar";
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
          onMouseEnter={() => setHoverSlot(isClickable ? key : null)}
          onMouseLeave={() => setHoverSlot(null)}
          onClick={() => {
            if (isClickable)
              alert(
                `Seleccionaste cancha ${cancha.nombre} ${slot.label} del ${date}`
              );
          }}
          title={tooltipText}
        >
          {hoverSlot === key && isClickable ? (
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
            <span className="legend-swatch occupied" /> No disponible
          </div>
          <div className="legend-item">
            <span className="legend-swatch no-turno" /> Disponible
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
    </div>
  );
}
