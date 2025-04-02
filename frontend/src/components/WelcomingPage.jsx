import React from "react";
import { Link } from "react-router-dom";

const WelcomePage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-blue-100 text-gray-900">
      <h1 className="text-4xl font-bold mb-6 text-center">
        Welcome to the Academic Issue Tracking System!
      </h1>
      <p className="text-lg text-center mb-8">
        Streamline academic issue reporting and resolution with ease. Whether you're a student, lecturer, or administrator, this platform is designed to make your work simpler and more efficient.
      </p>
      <div className="flex space-x-4">
        <Link to="/login">
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-500 transition">
            Login
          </button>
        </Link>
        <Link to="/signup">
          <button className="px-6 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-500 transition">
            Sign Up
          </button>
        </Link>
      </div>
    </div>
  );
};

export default WelcomePage;