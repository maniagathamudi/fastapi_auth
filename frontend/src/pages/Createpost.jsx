import { useState } from "react";
import DashboardLayout from "../layouts/Dashboardlayout";

function CreatePost() {

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [publishOption, setPublishOption] = useState("publish");
  const [scheduleDate, setScheduleDate] = useState("");
  const [scheduleTime, setScheduleTime] = useState("");

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      const token = localStorage.getItem("access_token");

      if (!token) {
        alert("Please login first");
        return;
      }

      const formData = new FormData();

      formData.append("title", title);
      formData.append("content", content);
      formData.append("publish_option", publishOption);

      if (publishOption === "schedule") {

        if (!scheduleDate || !scheduleTime) {
          alert("Select schedule date/time");
          return;
        }

        const scheduled_at = `${scheduleDate}T${scheduleTime}:00`;

        formData.append("scheduled_at", scheduled_at);
      }

      console.log("Submitting form...");

      const response = await fetch("http://127.0.0.1:8000/posts/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });

      const result = await response.json();

      console.log("Server Response:", result);

      if (!response.ok) {
        alert(result.detail || "Error creating post");
        return;
      }

      alert("Post Created Successfully 🎉");

      setTitle("");
      setContent("");
      setScheduleDate("");
      setScheduleTime("");
      setPublishOption("publish");

    } catch (error) {

      console.error(error);
      alert("Server error");

    }

  };

  return (

    <DashboardLayout>

      <div style={{ padding: "40px", color: "white" }}>

        <h2>Create Blog Post</h2>

        <form onSubmit={handleSubmit} style={{ maxWidth: "600px" }}>

          <label>Title</label>
          <input
            type="text"
            value={title}
            required
            onChange={(e) => setTitle(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "15px" }}
          />

          <label>Content</label>
          <textarea
            value={content}
            required
            onChange={(e) => setContent(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "15px" }}
          />

          <label>Publish Option</label>

          <select
            value={publishOption}
            onChange={(e) => setPublishOption(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "15px" }}
          >
            <option value="publish">Publish Now</option>
            <option value="draft">Save as Draft</option>
            <option value="schedule">Schedule</option>
          </select>

          {publishOption === "schedule" && (

            <>

              <label>Schedule Date</label>
              <input
                type="date"
                value={scheduleDate}
                onChange={(e) => setScheduleDate(e.target.value)}
                style={{ marginBottom: "10px", width: "100%", padding: "8px" }}
              />

              <label>Schedule Time</label>
              <input
                type="time"
                value={scheduleTime}
                onChange={(e) => setScheduleTime(e.target.value)}
                style={{ marginBottom: "15px", width: "100%", padding: "8px" }}
              />

            </>

          )}

          <button
            type="submit"
            style={{
              padding: "10px 20px",
              background: "#4f6cff",
              color: "white",
              border: "none",
              cursor: "pointer"
            }}
          >
            Create Post
          </button>

        </form>

      </div>

    </DashboardLayout>

  );

}

export default CreatePost;