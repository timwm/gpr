// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home"; // Import the Home page
import Dashboard from "./components/Dashboard"; // Import the Dashboard components
import Login from "./components/Login"; // Import the Login component
import Contact from "./pages/Contact"; // Import the Contact page
import About from "./pages/About"; // Import the About page
import Colleges from "./pages/Colleges"; // Import the Colleges page


function App() {
  return (
    <Router>
      {/* Define routes for the application */}
      <Routes>
        {/* Home Page */}
        <Route path="/" element={<Home />} />

        {/* Dashboard Page */}
        <Route path="/dashboard" element={<Dashboard userRole="student" />} />

        {/* Login Page */}
        <Route path="/login" element={<Login />} />

         {/* Contacts */}
         <Route path="/contacts" element={<Contact />} />

         {/* About */}
         <Route path="/about" element={<About />} />

         {/* Collegea */}
         <Route path="/colleges" element={<Colleges />} />
      </Routes>
    </Router>
  );
}

export default App;