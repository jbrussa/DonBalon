import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="site-header">
      <div className="brand">DonBalón</div>
      <nav className="nav">
        <a className="nav-link" href="#reservar">Reservar</a>
        <a className="nav-link" href="#torneos">Torneos</a>
        <a className="nav-cta" href="#login">Iniciar sesión</a>
      </nav>
    </header>
  );
};

export default Header;
