import React from "react";

const SkeletonPodCard = () => (
  <div
    className="card animate-pulse"
    style={{
      backgroundColor: "#343a40",
      borderRadius: "8px",
      overflow: "hidden",
      color: "white",
      maxWidth: "340px",
      height: "350px",
      boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
    }}
  >
    <div style={{ overflow: "hidden", height: "155px" }}>
      <div
        style={{
          backgroundColor: "#575c66",
          width: "100%",
          height: "100%",
        }}
      />
    </div>
    <div
      style={{
        padding: "16px",
        flex: "1",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          backgroundColor: "#575c66",
          height: "22px",
          width: "70%",
          marginBottom: "8px",
        }}
      />
      <div
        style={{ backgroundColor: "#4e555f", height: "18px", width: "85%" }}
      />
      <div
        style={{
          backgroundColor: "#4e555f",
          height: "18px",
          width: "30%",
          marginTop: "auto",
          marginBottom: "16px",
        }}
      />
      <div
        style={{
          marginTop: "auto",
          backgroundColor: "#d6336c",
          height: "38px",
          borderRadius: "4px",
        }}
      />
    </div>
  </div>
);

export default SkeletonPodCard;
