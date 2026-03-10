import { useEffect, useState } from "react";
import axios from "axios";
import "./Profile.css";

function Profile() {
  const [user, setUser] = useState({});
  const token = localStorage.getItem("token");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/profile", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setUser(res.data));
  }, []);

  return (
    <div className="profile-wrapper">
      <h1 className="welcome-text">
        Welcome back, {user.first_name}!
      </h1>

      <p className="profile-subtitle">
        Here’s a summary of your profile.
      </p>

      <div className="profile-card">
        <img
          src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
          className="avatar"
          alt="profile"
        />

        <div className="profile-details">
          <p>
            <span>Name:</span> {user.first_name} {user.last_name}
          </p>

          <p>
            <span>Email:</span> {user.email}
          </p>
        </div>
      </div>
    </div>
  );
}

export default Profile;