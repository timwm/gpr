import React, { useState, useEffect } from "react";

const RegistrarDashboard = () => {
  const [statistics, setStatistics] = useState({ totalStudents: 0, pendingIssues: 0 });

  useEffect(() => {
    // Simulate fetching registrar statistics
    const mockStatistics = { totalStudents: 1200, pendingIssues: 15 };
    setStatistics(mockStatistics);
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold mb-4">Registrar Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-blue-100 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold">Total Students</h2>
          <p className="text-2xl font-bold">{statistics.totalStudents}</p>
        </div>
        <div className="p-4 bg-yellow-100 rounded-lg shadow-md">
          <h2 className="text-lg font-semibold">Pending Issues</h2>
          <p className="text-2xl font-bold">{statistics.pendingIssues}</p>
        </div>
      </div>
    </div>
  );
};

export default RegistrarDashboard;
