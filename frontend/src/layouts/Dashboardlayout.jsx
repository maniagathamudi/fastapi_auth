import Navbar from "../components/Navbar";

function DashboardLayout({ children }) {

  return (

    <div style={{ minHeight: "100vh", backgroundColor: "#111827" }}>

      <Navbar />

      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "40px 20px"
        }}
      >
        {children}
      </div>

    </div>

  );

}

export default DashboardLayout;