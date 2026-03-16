import { Navigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

function ProtectedRoute({ children }) {

  const { isAuthenticated, isLoading } = useAuth0();

  // FIXED TOKEN NAME
  const token = localStorage.getItem("access_token");

  if (isLoading) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "20px"
        }}
      >
        Loading...
      </div>
    );
  }

  // Allow access if Auth0 login OR local JWT login
  if (!isAuthenticated && !token) {
    return <Navigate to="/" />;
  }

  return children;
}

export default ProtectedRoute;