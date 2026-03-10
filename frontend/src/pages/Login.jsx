import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const loginUser = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {

      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await API.post("/signin", formData);

      // store token
      localStorage.setItem("token", response.data.access_token);

      alert("Login Successful 🎉");

      navigate("/dashboard");

    } catch (error) {

      console.error(error);
      alert("Invalid email or password ❌");

    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        background: "#f5f5f5"
      }}
    >
      <form
        onSubmit={loginUser}
        style={{
          padding: "40px",
          border: "1px solid #ddd",
          borderRadius: "10px",
          width: "320px",
          textAlign: "center",
          background: "white",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
        }}
      >

        <h2 style={{ marginBottom: "20px" }}>Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "12px",
            borderRadius: "5px",
            border: "1px solid #ccc"
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
            borderRadius: "5px",
            border: "1px solid #ccc"
          }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "black",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer"
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        {/* Register Link */}
        <p style={{ marginTop: "15px", fontSize: "14px" }}>
          Don't have an account?{" "}
          <Link to="/register">Register</Link>
        </p>

      </form>
    </div>
  );
}

export default Login;