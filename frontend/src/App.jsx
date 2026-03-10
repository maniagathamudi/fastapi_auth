import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import MyPosts from "./pages/Mypost";
import AllPosts from "./pages/AllPosts";
import Plans from "./pages/Subscription";
import Profile from "./pages/profile";
import Comments from "./pages/comments";
import Likes from "./pages/Likes";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* Login Page */}
        <Route path="/" element={<Login />} />

        {/* Dashboard / Home */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* My Posts */}
        <Route
          path="/myposts"
          element={
            <ProtectedRoute>
              <MyPosts />
            </ProtectedRoute>
          }
        />

        {/* All Posts */}
        <Route
          path="/posts"
          element={
            <ProtectedRoute>
              <AllPosts />
            </ProtectedRoute>
          }
        />

        {/* Subscription Plans */}
        <Route
          path="/plans"
          element={
            <ProtectedRoute>
              <Plans />
            </ProtectedRoute>
          }
        />

        {/* Profile */}
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        {/* Comments */}
        <Route
          path="/comments"
          element={
            <ProtectedRoute>
              <Comments />
            </ProtectedRoute>
          }
        />

        {/* Likes */}
        <Route
          path="/likes"
          element={
            <ProtectedRoute>
              <Likes />
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>

  );

}

export default App;