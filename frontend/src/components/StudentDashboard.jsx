// src/components/StudentDashboard.js
// src/components/StudentDashboard.js
import React, { useState, useEffect } from "react";

import IssueForm from "./IssueForm";


import Notifications from "./Notifications";
import Navbar from "./Navbar";


const StudentDashboard = () => {
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    const fetchIssues = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:8000/api/issues/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setIssues(response.data);
      } catch (error) {
        console.error("Error fetching issues:", error);
      }
    };
    fetchIssues();
  }, []);

  return (
    <div>
      <Navbar />
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Student Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Log a New Issue</h2>
            <IssueForm />
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md col-span-2">
            <h2 className="text-xl font-semibold mb-4">Issue Tracking</h2>
            
            <ul>
              {issues.map((issue) => (
                <li key={issue.id}>{issue.title}</li>
              ))}
            </ul>
          </div>
        </div>
        <Notifications />
      </div>
    </div>
  );
};

export default StudentDashboard;