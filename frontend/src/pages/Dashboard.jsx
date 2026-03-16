import DashboardLayout from "../layouts/Dashboardlayout";
import "../styles/dashboard.css";

import {
Chart as ChartJS,
CategoryScale,
LinearScale,
BarElement,
ArcElement,
Title,
Tooltip,
Legend
} from "chart.js";

import { Bar, Pie } from "react-chartjs-2";

import { Link } from "react-router-dom";

ChartJS.register(
CategoryScale,
LinearScale,
BarElement,
ArcElement,
Title,
Tooltip,
Legend
);

function Dashboard() {

const totalPosts = 2;
const totalComments = 2;
const totalLikes = 4;

const barData = {
labels: ["Post 1", "Post 2"],
datasets: [
{
label: "Likes",
data: [2, 2],
backgroundColor: "#60a5fa"
},
{
label: "Comments",
data: [1, 1],
backgroundColor: "#fb7185"
}
]
};

const pieData = {
labels: ["Likes", "Comments"],
datasets: [
{
data: [totalLikes, totalComments],
backgroundColor: ["#4ade80", "#f87171"]
}
]
};

return (


<DashboardLayout>

  <div className="dashboard-container">

    <div className="dashboard-welcome">

      <h1>Welcome to your Dashboard 👋</h1>

      <p>
        Manage your blog posts, comments, likes and subscriptions.
      </p>

      <Link to="/create-post">

        <button
          style={{
            marginTop: "20px",
            padding: "12px 25px",
            fontSize: "16px",
            background: "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          ➕ Create New Post
        </button>

      </Link>

    </div>

    <div className="dashboard-stats">

      <div className="stat-card">
        <h3>Total Posts</h3>
        <p>{totalPosts}</p>
      </div>

      <div className="stat-card">
        <h3>Total Comments</h3>
        <p>{totalComments}</p>
      </div>

      <div className="stat-card">
        <h3>Total Likes</h3>
        <p>{totalLikes}</p>
      </div>

    </div>

    <div className="charts-container">

      <div className="chart-card">
        <h3>Likes vs Comments</h3>
        <Bar data={barData} />
      </div>

      <div className="chart-card">
        <h3>Engagement Distribution</h3>
        <Pie data={pieData} />
      </div>

    </div>

  </div>

</DashboardLayout>


);
}

export default Dashboard;
