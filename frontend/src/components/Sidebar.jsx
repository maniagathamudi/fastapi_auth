function Sidebar({ setPage }) {

  return (

    <div style={{
      width: "220px",
      background: "#111",
      color: "white",
      padding: "20px",
      height: "100vh"
    }}>

      <h2>Dashboard</h2>

      <p onClick={() => setPage("posts")} style={{cursor:"pointer"}}>Posts</p>
      <p onClick={() => setPage("comments")} style={{cursor:"pointer"}}>Comments</p>
      <p onClick={() => setPage("likes")} style={{cursor:"pointer"}}>Likes</p>
      <p onClick={() => setPage("subscriptions")} style={{cursor:"pointer"}}>Subscriptions</p>
      <p onClick={() => setPage("profile")} style={{cursor:"pointer"}}>Profile</p>

    </div>

  );
}

export default Sidebar;