// src/components/Button.js
import React from "react";

const Button = ({ label, onClick, type = "button", className = "", isInactive = false }) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={isInactive}
      className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150 ease-in-out ${className}`}
    >
      {label}
    </button>
  );
};

export default Button;