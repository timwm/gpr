// src/components/Notifications.js
import React from "react";

const Notifications = () => {
  const notifications = [
    "Issue #1 updated to 'Pending'.",
    "Issue #2 resolved.",
  ];

  return (
    <div className="fixed bottom-4 right-4">
      <div className="bg-white p-4 rounded-lg shadow-lg">
        <h3 className="text-lg font-semibold mb-2">Notifications</h3>
        <ul>
          {notifications.map((notification, index) => (
            <li key={index} className="text-sm text-gray-700">
              {notification}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Notifications;