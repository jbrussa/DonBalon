import React from 'react';
import './ActionButton.css';

const ActionButton = ({ children, onClick, primary }) => {
  return (
    <button className={primary ? 'btn btn-primary' : 'btn'} onClick={onClick}>
      {children}
    </button>
  );
};

export default ActionButton;
