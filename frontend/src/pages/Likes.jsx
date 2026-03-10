import { useEffect, useState } from "react";
import axios from "axios";
import DashboardLayout from "../layouts/Dashboardlayout";

function Likes() {

  const [likes, setLikes] = useState([]);

  useEffect(() => {
    fetchLikes();
  }, []);

  const fetchLikes = async () => {

    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:8000/likes/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setLikes(res.data);

    } catch (error) {
      console.log(error);
    }

  };

  return (
    <DashboardLayout>

      <h1>My Likes</h1>

      {likes.map((like) => (

        <div key={like.id} style={{marginBottom:"20px"}}>

          👍 <strong>Post ID:</strong> {like.post_id}

        </div>

      ))}

    </DashboardLayout>
  );
}

export default Likes;