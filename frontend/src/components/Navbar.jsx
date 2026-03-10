import { useNavigate } from "react-router-dom";

function Navbar() {

  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (

    <div style={{
      display:"flex",
      justifyContent:"space-between",
      alignItems:"center",
      padding:"15px 40px",
      background:"#0b1a36",
      color:"white"
    }}>

      <h2 style={{color:"#7c8cff"}}>BlogPlatform</h2>

      <div style={{display:"flex",gap:"25px",cursor:"pointer"}}>

        <span onClick={()=>navigate("/dashboard")}>Home</span>

        <span onClick={()=>navigate("/myposts")}>My Posts</span>

        <span onClick={()=>navigate("/profile")}>Profile</span>

        <span onClick={()=>navigate("/plans")}>Subscription</span>

        <span onClick={()=>navigate("/comments")}>Comments</span>

        <span onClick={()=>navigate("/likes")}>Likes</span>

      </div>

      <button
        onClick={logout}
        style={{
          background:"#ff4b4b",
          border:"none",
          color:"white",
          padding:"8px 16px",
          borderRadius:"6px"
        }}
      >
        Logout
      </button>

    </div>

  );

}

export default Navbar;