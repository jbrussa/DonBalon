import React from "react";
import "./Location.css";

export default function Location() {
  const address =
    "Complejo de Canchas de Fútbol Don Balón, Manuel Cardeñosa 4400, X5000 Córdoba, Argentina";
  const mapsQuery = encodeURIComponent(address);

  return (
    <section className="location-root">
      <h2 className="location-title">Donde estamos</h2>

      <div className="location-grid">
        <div className="location-map">
          {/* If you don't have an API key, using the plain maps.google.com URL also works as iframe src.
              Replace YOUR_API_KEY above or change to a public embed URL. */}
          <iframe
            title="DonBalon Location"
            src={`https://www.google.com/maps?q=${mapsQuery}&output=embed`}
            style={{
              display: "block",
              width: "100%",
              height: 540,
              border: 0,
              borderRadius: 10,
            }}
            loading="lazy"
          />
        </div>

        <div className="location-side">
          <div className="info-card">
            <h4>Ubicación</h4>
            <p>{address}</p>
          </div>

          <div className="info-card">
            <h4>Horarios del Club</h4>
            <ul className="hours-list">
              <li>
                <strong>Lunes, Martes, Miercoles, Jueves</strong>: 17:00 a 00:00
              </li>
              <li>
                <strong>Viernes</strong>: 17:00 a 23:00
              </li>
              <li>
                <strong>Domingo</strong>: 17:00 a 22:00
              </li>
              <li>
                <strong>Sabado</strong>: 11:00 a 21:00
              </li>
              <li>
                <strong>Feriados</strong>: 14:00 a 22:00
              </li>
            </ul>
          </div>

          <div className="info-card">
            <h4>Servicios del Club</h4>
            <div className="services-grid">
              <div className="svc">Wi‑Fi</div>
              <div className="svc">Vestuarios</div>
              <div className="svc">Estacionamiento</div>
              <div className="svc">Torneos</div>
              <div className="svc">Parrilla</div>
              <div className="svc">Escuelita</div>
              <div className="svc">Bar / Restaurante</div>
              <div className="svc">Quincho</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
