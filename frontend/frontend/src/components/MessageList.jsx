import { useEffect, useRef } from "react";

const MessageList = ({ messages, currentUser }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="no-messages">
          <p>NO MESSAGES YET</p>
          <p>START THE CONVERSATION</p>
        </div>
      ) : (
        messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.username === currentUser ? "message-own" : "message-other"
            }`}
          >
            <div className="message-header">
              <span className="message-user">{msg.username}</span>
              <span className="message-time">{formatTime(msg.timestamp)}</span>
            </div>
            <div className="message-content">{msg.content}</div>
          </div>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
