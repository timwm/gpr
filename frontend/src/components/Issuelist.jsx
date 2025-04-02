// src/components/IssueList.js
// src/components/IssueList.js
import React from "react";
import Button from "./Button"; // Import the Button component

const IssueList = ({ issues, onAssign, onResolve }) => {
  return (
    <table className="w-full">
      <thead>
        <tr className="bg-gray-200">
          <th className="p-2">ID</th>
          <th className="p-2">Type</th>
          <th className="p-2">Status</th>
          <th className="p-2">Date</th>
          <th className="p-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        {issues.map((issue) => (
          <tr key={issue.id} className="border-b">
            <td className="p-2">{issue.id}</td>
            <td className="p-2">{issue.category}</td>
            <td className="p-2">{issue.status}</td>
            <td className="p-2">{new Date(issue.created_at).toLocaleDateString()}</td>
            <td className="p-2 space-x-2">
              {onAssign && (
                <Button label="Assign" onClick={() => onAssign(issue.id, 1)} />
              )}
              {onResolve && (
                <Button label="Resolve" onClick={() => onResolve(issue.id)} />
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default IssueList;