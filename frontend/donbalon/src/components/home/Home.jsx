import React from "react";
import "./Home.css";
import Header from "../layout/Header";
import ActionButton from "../shared/ActionButton";
import Schedule from "../schedule/Schedule";
import Carousel from "../carousel/Carousel";
import Location from "../location/Location";
import Footer from "../layout/Footer";

const Home = () => {
  return (
    <div className="home-root">
      <Header />

      <main className="home-hero">
        <div className="hero-content hero-center">
          <h1 className="hero-title">DonBalón</h1>
          <p className="hero-sub">
            Reserva canchas y participa en torneos con la mejor experiencia.
          </p>

          <div className="hero-ctas">
            <ActionButton
              onClick={() => {
                const el = document.getElementById("schedule");
                if (el)
                  el.scrollIntoView({ behavior: "smooth", block: "start" });
              }}
              primary
            >
              Reservar cancha
            </ActionButton>
          </div>
        </div>

        {/* right column intentionally removed; promo cards will appear below the CTAs */}
      </main>

      {/* Promo cards placed between hero CTAs and the carousel */}
      <section className="promo-section">
        <div className="promo-row">
          <div className="promo-card">
            <h4>Horarios flexibles</h4>
            <p>Encuentra y reserva el turno que mejor te quede.</p>
          </div>
          <div className="promo-card">
            <h4>Reservas online</h4>
            <p>Reserva tu cancha en segundos desde cualquier dispositivo.</p>
          </div>
          <div className="promo-card">
            <h4>Servicios en cancha</h4>
            <p>Bebidas, alquiler de implementos y más disponibles.</p>
          </div>
          <div className="promo-card">
            <h4>Eventos y torneos</h4>
            <p>Participa en encuentros y campeonatos organizados.</p>
          </div>
        </div>
      </section>

      {/* Carousel placed before the schedule as requested */}
      <section className="carousel-section" style={{ padding: "0 16px 24px" }}>
        <Carousel folder="/photos" interval={4500} />
      </section>

      <section id="schedule" className="schedule-section">
        <h2 style={{ marginLeft: 16 }}>Elige tu turno</h2>
        <div style={{ padding: "0 16px 32px" }}>
          <Schedule />
        </div>
      </section>

      {/* Location section below schedule */}
      <Location />

      {/* Small footer to visually finish the page */}
      <Footer />
    </div>
  );
};

export default Home;
