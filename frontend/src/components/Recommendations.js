import React from "react";

const Recommendations = ({ text }) => {
  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h2 style={{ color: "#1976d2" }}>AI Recommendations</h2>
      <p style={{ fontSize: "16px", lineHeight: "1.5" }}>{text}</p>
    </div>
  );
};

export default Recommendations;
