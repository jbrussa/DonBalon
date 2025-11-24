import React from "react";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-left">© {new Date().getFullYear()} DonBalón</div>
        <div className="footer-right">
          Hecho con ♥ ·{" "}
          <a href="#" onClick={(e) => e.preventDefault()}>
            Contacto
          </a>
        </div>
      </div>
    </footer>
  );
}
