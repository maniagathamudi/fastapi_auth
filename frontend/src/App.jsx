import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import MyPosts from "./pages/Mypost";
import AllPosts from "./pages/AllPosts";
import Plans from "./pages/Subscription";
import Profile from "./pages/profile";
import Comments from "./pages/comments";
import Likes from "./pages/Likes";
import Register from "./pages/register";
import AIChat from "./components/AIChat";
import ProtectedRoute from "./components/ProtectedRoute";
import CreatePost from "./pages/createpost";

function App() {

const { isLoading } = useAuth0();
const token = localStorage.getItem("token");

if (isLoading) {
return (
<div style={{ textAlign: "center", marginTop: "100px" }}>
Loading... </div>
);
}

return (
<> <Routes>


    {/* LOGIN */}
    <Route
      path="/"
      element={!token ? <Login /> : <Navigate to="/dashboard" />}
    />

    <Route
      path="/register"
      element={!token ? <Register /> : <Navigate to="/dashboard" />}
    />

    {/* DASHBOARD */}
    <Route
      path="/dashboard"
      element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      }
    />

    {/* POSTS */}
    <Route
      path="/myposts"
      element={
        <ProtectedRoute>
          <MyPosts />
        </ProtectedRoute>
      }
    />

    <Route
      path="/posts"
      element={
        <ProtectedRoute>
          <AllPosts />
        </ProtectedRoute>
      }
    />

    {/* CREATE POST */}
    <Route
      path="/create-post"
      element={
        <ProtectedRoute>
          <CreatePost />
        </ProtectedRoute>
      }
    />

    {/* OTHER PAGES */}
    <Route
      path="/plans"
      element={
        <ProtectedRoute>
          <Plans />
        </ProtectedRoute>
      }
    />

    <Route
      path="/profile"
      element={
        <ProtectedRoute>
          <Profile />
        </ProtectedRoute>
      }
    />

    <Route
      path="/comments"
      element={
        <ProtectedRoute>
          <Comments />
        </ProtectedRoute>
      }
    />

    <Route
      path="/likes"
      element={
        <ProtectedRoute>
          <Likes />
        </ProtectedRoute>
      }
    />

  </Routes>

  <AIChat />
</>


);
}

export default App;
