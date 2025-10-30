import { useRef, useEffect } from "react";

const MessageList = ({ messages, currentUser }) => {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Group messages by date
  const groupMessagesByDate = (messages) => {
    const groups = [];
    let currentDate = null;

    messages.forEach((message) => {
      const messageDate = new Date(message.timestamp).toDateString();

      if (messageDate !== currentDate) {
        currentDate = messageDate;
        groups.push({ type: "date", date: messageDate });
      }

      groups.push({ type: "message", data: message });
    });

    return groups;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date().toDateString();
    const yesterday = new Date(Date.now() - 86400000).toDateString();

    if (dateString === today) return "TODAY";
    if (dateString === yesterday) return "YESTERDAY";

    return date
      .toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })
      .toUpperCase();
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  };

  const groupedMessages = groupMessagesByDate(messages);

  if (messages.length === 0) {
    return (
      <div className="message-list">
        <div className="no-messages">
          <p>NO MESSAGES YET</p>
          <p>START THE CONVERSATION</p>
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      {groupedMessages.map((item, index) => {
        if (item.type === "date") {
          return (
            <div key={`date-${index}`} className="date-separator">
              <span>{formatDate(item.date)}</span>
            </div>
          );
        }

        const message = item.data;
        const isOwn = message.username === currentUser;

        return (
          <div
            key={index}
            className={isOwn ? "message message-own" : "message message-other"}
          >
            <div className="message-header">
              <span className="message-user">{message.username}</span>
              <span className="message-time">
                {formatTime(message.timestamp)}
              </span>
            </div>
            <div className="message-content">{message.content}</div>
          </div>
        );
      })}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
