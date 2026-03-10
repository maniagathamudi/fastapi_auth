import { useEffect, useState } from "react";
import API from "../api";

function MyPosts() {

  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {

    try {

      const response = await API.get("/posts/");

      setPosts(response.data.data); // important

    } catch (error) {

      console.log(error);

    }

  };

  return (

    <div style={{padding:"20px"}}>

      <h1 style={{fontSize:"40px",marginBottom:"30px"}}>My Posts</h1>

      {posts.map((post) => (

        <div
          key={post.id}
          style={{
            background:"#0b1a33",
            padding:"25px",
            borderRadius:"12px",
            marginBottom:"25px"
          }}
        >

          <h2>{post.title}</h2>

          <p>{post.content}</p>

          {post.image && (

            <img
              src={post.image}
              alt="post"
              style={{
                width:"400px",
                borderRadius:"10px",
                marginTop:"10px"
              }}
            />

          )}

          <div style={{marginTop:"15px"}}>

            👍 Like ({post.likes_count})

            <span style={{marginLeft:"20px"}}>
              💬 Comments ({post.comments_count})
            </span>

          </div>

        </div>

      ))}

    </div>

  );

}

export default MyPosts;