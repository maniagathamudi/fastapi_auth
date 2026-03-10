import { useEffect, useState } from "react";
import API from "../api";
import Navbar from "../components/Navbar";

function AllPosts(){

  const [posts,setPosts] = useState([]);

  useEffect(()=>{

    const fetchPosts = async ()=>{

      const res = await API.get("/posts");

      setPosts(res.data);

    };

    fetchPosts();

  },[]);

  return(

    <div>

      <Navbar/>

      <h2>All Posts</h2>

      {posts.map(post => (

        <div key={post.id}>

          <h3>{post.title}</h3>
          <p>{post.content}</p>

        </div>

      ))}

    </div>

  );
}

export default AllPosts;