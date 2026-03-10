import { useState } from "react";
import "./Dashboard.css";

function Subscription() {

  const [message, setMessage] = useState("");

  const choosePlan = (plan) => {
    setMessage(`🎉 ${plan} plan activated successfully!`);

    setTimeout(() => {
      setMessage("");
    }, 2500);
  };

  return (
    <div style={pageStyle}>

      <h1 style={titleStyle}>Subscription Plans</h1>

      <div style={containerStyle}>

        {/* Basic */}
        <div style={cardStyle}>
          <h2>Basic</h2>
          <p>Price ₹199</p>
          <p>Post Limit: 1</p>
          <p>Image Limit: 1</p>
          <p>Like Limit: 5</p>
          <p>Comment Limit: 5</p>
          <button style={btnStyle} onClick={() => choosePlan("Basic")}>
            Choose Plan
          </button>
        </div>

        {/* Premium */}
        <div style={cardStyle}>
          <h2>Premium</h2>
          <p>Price ₹499</p>
          <p>Post Limit: 5</p>
          <p>Image Limit: 5</p>
          <p>Like Limit: 20</p>
          <p>Comment Limit: 20</p>
          <button style={btnStyle} onClick={() => choosePlan("Premium")}>
            Choose Plan
          </button>
        </div>

        {/* Pro */}
        <div style={cardStyle}>
          <h2>Pro</h2>
          <p>Price ₹999</p>
          <p>Post Limit: 9999</p>
          <p>Image Limit: 9999</p>
          <p>Like Limit: 9999</p>
          <p>Comment Limit: 9999</p>
          <button style={btnStyle} onClick={() => choosePlan("Pro")}>
            Choose Plan
          </button>
        </div>

      </div>

      {/* Popup message */}
      {message && (
        <div style={popupStyle}>
          {message}
        </div>
      )}

    </div>
  );
}

/* PAGE STYLE */
const pageStyle = {
  minHeight: "100vh",
  padding: "60px",
  textAlign: "center",
  background: "linear-gradient(135deg,#020617,#0f172a,#1e293b)",
  color: "white"
};

/* TITLE */
const titleStyle = {
  fontSize: "48px",
  marginBottom: "50px"
};

/* CARDS CONTAINER */
const containerStyle = {
  display: "flex",
  gap: "30px",
  justifyContent: "center",
  flexWrap: "wrap"
};

/* CARD */
const cardStyle = {
  background: "#0f172a",
  padding: "30px",
  width: "280px",
  borderRadius: "12px",
  textAlign: "left",
  border: "1px solid rgba(255,255,255,0.1)",
  boxShadow: "0 10px 25px rgba(0,0,0,0.6)",
  transition: "0.3s"
};

/* BUTTON */
const btnStyle = {
  marginTop: "20px",
  padding: "10px 20px",
  background: "#3b82f6",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  fontWeight: "600"
};

/* POPUP */
const popupStyle = {
  position: "fixed",
  bottom: "40px",
  left: "50%",
  transform: "translateX(-50%)",
  background: "#22c55e",
  padding: "15px 30px",
  borderRadius: "10px",
  fontSize: "18px",
  boxShadow: "0 5px 20px rgba(0,0,0,0.5)"
};

export default Subscription;