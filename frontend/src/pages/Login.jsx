import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import API from "../api";

function Login() {

  const navigate = useNavigate();
  const { loginWithRedirect, isAuthenticated, user, isLoading } = useAuth0();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      console.log("Auth0 User:", user);
      navigate("/dashboard");
    }
  }, [isAuthenticated, user, navigate]);

  const loginUser = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {

      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await API.post("/signin", formData);

      // FIXED TOKEN STORAGE
      localStorage.setItem("access_token", response.data.access_token);

      alert("Login Successful 🎉");

      navigate("/dashboard");

    } catch (error) {

      console.error(error);
      alert("Invalid email or password ❌");

    } finally {
      setLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontSize: "20px"
      }}>
        Loading...
      </div>
    );
  }

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg,#0f2027,#203a43,#2c5364)",
        fontFamily: "Segoe UI"
      }}
    >

      <form
        onSubmit={loginUser}
        style={{
          padding: "40px",
          borderRadius: "14px",
          width: "360px",
          textAlign: "center",
          background: "rgba(255,255,255,0.08)",
          backdropFilter: "blur(10px)",
          boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
          color: "white"
        }}
      >

        <h1 style={{ color: "#7c8cff", marginBottom: "5px" }}>
          BlogPlatform
        </h1>

        <p style={{ color: "#ccc", marginBottom: "25px" }}>
          Welcome back 👋
        </p>

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "15px",
            borderRadius: "8px",
            border: "none",
            background: "#1e2a44",
            color: "white",
            outline: "none"
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
            padding: "12px",
            marginBottom: "18px",
            borderRadius: "8px",
            border: "none",
            background: "#1e2a44",
            color: "white",
            outline: "none"
          }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: "12px",
            background: "#4f6cff",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontSize: "16px",
            cursor: "pointer",
            marginBottom: "18px"
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p style={{ margin: "15px 0", color: "#aaa" }}>OR</p>

        <button
          type="button"
          onClick={() =>
            loginWithRedirect({
              authorizationParams: { connection: "google-oauth2" }
            })
          }
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "10px",
            background: "#ea4335",
            color: "white",
            border: "none",
            borderRadius: "8px"
          }}
        >
          Continue with Google
        </button>

        <button
          type="button"
          onClick={() =>
            loginWithRedirect({
              authorizationParams: { connection: "facebook" }
            })
          }
          style={{
            width: "100%",
            padding: "12px",
            background: "#1877f2",
            color: "white",
            border: "none",
            borderRadius: "8px"
          }}
        >
          Continue with Facebook
        </button>

        <p style={{ marginTop: "20px", fontSize: "14px", color: "#ccc" }}>
          Don't have an account?{" "}
          <Link to="/register" style={{ color: "#7c8cff" }}>
            Register
          </Link>
        </p>

      </form>

    </div>
  );
}

export default Login;