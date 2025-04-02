// src/components/IssueForm.js

  // src/components/IssueForm.js
import React, { useState } from "react";

import Button from "./Button"; // Import the Button component

const IssueForm = () => {
  const [issue, setIssue] = useState({
    category: "",
    description: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      
        const response = await fetch("/api/issues", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(issue),
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
      
      alert("Issue submitted successfully!");
      setIssue({ category: "", description: "" });
    } catch (error) {
      console.error("Error submitting issue:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-gray-700">Issue Type</label>
        <select
          className="w-full p-2 border rounded"
          value={issue.category}
          onChange={(e) => setIssue({ ...issue, category: e.target.value })}
          required
        >
          <option value="">Select</option>
          <option value="missing_marks">Missing Marks</option>
          <option value="appeal">Appeal</option>
          <option value="correction">Correction</option>
        </select>
      </div>
      <div>
        <label className="block text-gray-700">Description</label>
        <textarea
          className="w-full p-2 border rounded"
          rows="4"
          value={issue.description}
          onChange={(e) => setIssue({ ...issue, description: e.target.value })}
          required
        ></textarea>
      </div>
      <Button label="Submit" type="submit" className="w-full" />
    </form>
  );
};

export default IssueForm;       