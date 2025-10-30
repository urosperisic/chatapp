import { useState, useEffect, useRef, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import OnlineUsersModal from "../components/OnlineUsersModal";

const ChatPage = () => {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [room, _setRoom] = useState("general");
  const [isConnected, setIsConnected] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const ws = useRef(null);

  const token = localStorage.getItem("access_token");

  // Determine API URL based on environment
  const API_URL =
    window.location.hostname === "localhost"
      ? "http://localhost:8000"
      : window.location.origin;

  // Determine WebSocket URL based on environment
  const WS_PROTOCOL = window.location.protocol === "https:" ? "wss:" : "ws:";
  const WS_HOST =
    window.location.hostname === "localhost"
      ? "localhost:8000"
      : window.location.host;

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/chat/rooms/${room}/messages/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const data = await response.json();
        if (data.status === "success") {
          setMessages(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch message history:", error);
      }
    };

    fetchHistory();

    const wsUrl = `${WS_PROTOCOL}//${WS_HOST}/ws/chat/${room}/`;
    ws.current = new WebSocket(wsUrl, ["authorization", token]);

    ws.current.onopen = () => {
      setIsConnected(true);
      setOnlineUsers((prev) => [...new Set([...prev, user?.username])]);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "message") {
        setMessages((prev) => [
          ...prev,
          {
            username: data.username,
            content: data.message,
            timestamp: data.timestamp,
          },
        ]);
      } else if (data.type === "user_online") {
        if (data.action === "joined") {
          setOnlineUsers((prev) => [...new Set([...prev, data.username])]);
        } else if (data.action === "left") {
          setOnlineUsers((prev) => prev.filter((u) => u !== data.username));
        }
      }
    };

    ws.current.onerror = () => {
      setIsConnected(false);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      setOnlineUsers([]);
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [room, token, user, API_URL, WS_PROTOCOL, WS_HOST]);

  const sendMessage = (content) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ message: content }));
    }
  };

  return (
    <>
      <div className="chat-container">
        <div className="chat-header">
          <h1>CHAT ROOM: {room.toUpperCase()}</h1>
          <div className="connection-status">
            <span
              className={
                isConnected ? "status-connected" : "status-disconnected"
              }
            >
              {isConnected ? "● ONLINE" : "● OFFLINE"}
            </span>
            <button
              className="online-users-button"
              onClick={() => setIsModalOpen(true)}
              aria-label="View online users"
            >
              👥 {onlineUsers.length} ONLINE
            </button>
            <span className="username">USER: {user?.username}</span>
          </div>
        </div>

        <MessageList messages={messages} currentUser={user?.username} />
        <MessageInput onSend={sendMessage} disabled={!isConnected} />
      </div>

      <OnlineUsersModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        users={onlineUsers}
        currentUser={user?.username}
      />
    </>
  );
};

export default ChatPage;
