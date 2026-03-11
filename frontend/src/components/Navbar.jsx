import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import AIChat from "./AIChat";

function Navbar() {

  const navigate = useNavigate();

  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  const token = localStorage.getItem("token");

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  // Fetch notifications
  const getNotifications = async () => {
    try {

      const res = await fetch("http://127.0.0.1:8000/notifications/", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();

      setNotifications(data);

      // Count unread notifications
      const unread = data.filter((n) => n.is_read === 0).length;
      setUnreadCount(unread);

    } catch (error) {
      console.error("Notification error:", error);
    }
  };

  // Mark all notifications as read
  const markAllRead = async () => {

    try {

      await fetch("http://127.0.0.1:8000/notifications/mark-read", {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      getNotifications();

    } catch (error) {
      console.error("Mark read error:", error);
    }
  };

  useEffect(() => {

    getNotifications();

    // Auto refresh notifications every 5 seconds
    const interval = setInterval(() => {
      getNotifications();
    }, 5000);

    return () => clearInterval(interval);

  }, []);

  return (

    <div style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "15px 40px",
      background: "#0b1a36",
      color: "white"
    }}>

      <h2 style={{ color: "#7c8cff", cursor: "pointer" }}
          onClick={() => navigate("/home")}
      >
        BlogPlatform
      </h2>

      <div style={{ display: "flex", gap: "25px", cursor: "pointer" }}>

        <span onClick={() => navigate("/home")}>Home</span>
        <span onClick={() => navigate("/dashboard")}>Dashboard</span>
        <span onClick={() => navigate("/myposts")}>My Posts</span>
        <span onClick={() => navigate("/profile")}>Profile</span>
        <span onClick={() => navigate("/plans")}>Subscription</span>
        <span onClick={() => navigate("/comments")}>Comments</span>
        <span onClick={() => navigate("/likes")}>Likes</span>

      </div>


      {/* Right side */}
      <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>

        {/* Notification Bell */}
        <div style={{ position: "relative" }}>

          <span
            style={{ fontSize: "22px", cursor: "pointer" }}
            onClick={() => setShowNotifications(!showNotifications)}
          >
            🔔
          </span>

          {/* Red Badge */}
          {unreadCount > 0 && (
            <span
              style={{
                position: "absolute",
                top: "-5px",
                right: "-8px",
                background: "red",
                color: "white",
                borderRadius: "50%",
                padding: "2px 6px",
                fontSize: "12px",
                fontWeight: "bold"
              }}
            >
              {unreadCount}
            </span>
          )}

          {showNotifications && (
            <div style={{
              position: "absolute",
              right: 0,
              top: "35px",
              width: "300px",
              background: "#1f2c44",
              borderRadius: "10px",
              padding: "15px"
            }}>

              <div style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "10px"
              }}>
                <b>Notifications</b>

                <button
                  onClick={markAllRead}
                  style={{
                    background: "#3b6df6",
                    border: "none",
                    padding: "5px 10px",
                    color: "white",
                    borderRadius: "5px",
                    cursor: "pointer"
                  }}
                >
                  Mark All Read
                </button>
              </div>

              {notifications.length === 0 ? (
                <p>No notifications</p>
              ) : (
                notifications.map((n) => (
                  <div
                    key={n.id}
                    style={{
                      padding: "8px",
                      borderBottom: "1px solid #444"
                    }}
                  >
                    {n.message}
                  </div>
                ))
              )}

            </div>
          )}

        </div>

        {/* Logout */}
        <button
          onClick={logout}
          style={{
            background: "#ff4b4b",
            border: "none",
            color: "white",
            padding: "8px 16px",
            borderRadius: "6px",
            cursor: "pointer"
          }}
        >
          Logout
        </button>

      </div>

    </div>

  );
}
<AIChat />

export default Navbar;