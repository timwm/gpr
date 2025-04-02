// src/components/Navbar.js
import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/dashboard" className="text-2xl font-bold">
          AITS
        </Link>
        <div className="space-x-4">
          <Link to="/dashboard" className="hover:text-gray-200">
            Dashboard
          </Link>
          <Link to="/" className="hover:text-gray-200">
            Logout
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;