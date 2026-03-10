import { useEffect, useState } from "react";
import axios from "axios";
import DashboardLayout from "../layouts/Dashboardlayout";

function Comments() {

  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetchComments();
  }, []);

  const fetchComments = async () => {
    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:8000/comments/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setComments(res.data);

    } catch (error) {
      console.log(error);
    }
  };

  return (
    <DashboardLayout>

      <h1>My Comments</h1>

      {comments.map((comment) => (

        <div key={comment.id} style={{marginBottom:"20px"}}>

          <p><strong>Post ID:</strong> {comment.post_id}</p>

          <p>💬 {comment.content}</p>

        </div>

      ))}

    </DashboardLayout>
  );
}

export default Comments;