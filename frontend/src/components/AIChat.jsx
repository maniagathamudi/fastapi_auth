import { useState } from "react";
import axios from "axios";

function AIChat() {

  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async (customMsg = null) => {

    const msg = customMsg || message;

    if (!msg.trim()) return;

    const token = localStorage.getItem("token");

    // Add user message
    setChat((prev) => [...prev, { sender: "user", text: msg }]);

    setMessage("");

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/api/ai-support/",
        { message: msg },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        }
      );

      const aiAnswer = res.data.answer;
      const options = res.data.options || [];

      // Add AI response
      setChat((prev) => [
        ...prev,
        {
          sender: "ai",
          text: aiAnswer,
          options: options
        }
      ]);

    } catch (err) {

      setChat((prev) => [
        ...prev,
        { sender: "ai", text: "AI service unavailable." }
      ]);

    }

  };

  return (
    <>
      {/* Chat Button */}
      <div
        onClick={() => setOpen(!open)}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          width: "60px",
          height: "60px",
          background: "#2563eb",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontSize: "26px",
          cursor: "pointer",
          boxShadow: "0 6px 20px rgba(0,0,0,0.4)"
        }}
      >
        💬
      </div>

      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "90px",
            right: "20px",
            width: "340px",
            height: "450px",
            background: "#0f172a",
            borderRadius: "12px",
            padding: "15px",
            color: "white",
            display: "flex",
            flexDirection: "column",
            boxShadow: "0 10px 30px rgba(0,0,0,0.5)"
          }}
        >

          <h3 style={{ marginBottom: "10px" }}>🤖 AI Support</h3>

          {/* Messages */}
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              marginBottom: "10px"
            }}
          >

            {chat.map((c, i) => (

              <div key={i} style={{ marginBottom: "10px" }}>

                {/* User message */}
                {c.sender === "user" && (
                  <div
                    style={{
                      textAlign: "right"
                    }}
                  >
                    <span
                      style={{
                        background: "#2563eb",
                        padding: "8px 12px",
                        borderRadius: "12px",
                        display: "inline-block"
                      }}
                    >
                      {c.text}
                    </span>
                  </div>
                )}

                {/* AI message */}
                {c.sender === "ai" && (
                  <div>

                    <span
                      style={{
                        background: "#334155",
                        padding: "8px 12px",
                        borderRadius: "12px",
                        display: "inline-block"
                      }}
                    >
                      {c.text}
                    </span>

                    {/* AI options */}
                    {c.options && c.options.length > 0 && (
                      <div
                        style={{
                          marginTop: "6px",
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "5px"
                        }}
                      >
                        {c.options.map((opt, index) => (
                          <button
                            key={index}
                            onClick={() => sendMessage(opt)}
                            style={{
                              background: "#2563eb",
                              border: "none",
                              padding: "5px 8px",
                              borderRadius: "6px",
                              color: "white",
                              cursor: "pointer",
                              fontSize: "12px"
                            }}
                          >
                            {opt}
                          </button>
                        ))}
                      </div>
                    )}

                  </div>
                )}

              </div>

            ))}

          </div>

          {/* Input */}
          <div
            style={{
              display: "flex",
              gap: "6px"
            }}
          >

            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask something..."
              style={{
                flex: 1,
                padding: "8px",
                borderRadius: "6px",
                border: "none",
                outline: "none"
              }}
            />

            <button
              onClick={() => sendMessage()}
              style={{
                background: "#2563eb",
                border: "none",
                padding: "8px 12px",
                borderRadius: "6px",
                color: "white",
                cursor: "pointer"
              }}
            >
              Send
            </button>

          </div>

        </div>
      )}
    </>
  );
}

export default AIChat;