// src/components/Dashboard.js
import React from "react";
import IssueForm from "./IssueForm";
import IssueTable from "./IssueTable";
import Colleges from "../pages/Colleges";
import Home from "../pages/Home";
import About from "../pages/About";

import Navbar from "./Navbar";


import Button from "./Button";

const Dashboard = ({ userRole }) => {
  return (
    <div className="flex flex-row">
      <div className="grow-1 pl-4">
        <ul>
        <li><a href="#s">Colleges</a></li>
        <li><a href="#g">About</a></li>
        <li><a href="#h">Home</a></li>
        <li><a href="#h">Navbar</a></li>
        
        </ul>
      </div>
      <div className="bg-gray-200 min-h-screen p-4 grow-2 ">
        <h1 className="text-2xl font-bold mb-4">Welcome to AITS</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Issue Logging Form for Students */}
          {userRole === "student" && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-4">Log a New Issue</h2>
              <IssueForm />
              <Button text="Submit Issue" />
            </div>
          )}

          {/* Issue Tracking Table */}
          <div className="bg-white p-6 rounded-lg shadow-md col-span-2">
            <h2 className="text-xl font-semibold mb-4">Issue Tracking</h2>
            <IssueTable userRole={userRole} />
          </div>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;
