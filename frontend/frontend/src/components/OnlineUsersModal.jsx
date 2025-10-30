const OnlineUsersModal = ({ isOpen, onClose, users, currentUser }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>ONLINE USERS ({users.length})</h2>
          <button
            onClick={onClose}
            className="modal-close"
            aria-label="Close modal"
          >
            ✕
          </button>
        </div>
        <div className="modal-body">
          {users.length === 0 ? (
            <p className="no-users">NO USERS ONLINE</p>
          ) : (
            <ul className="user-list">
              {users.map((username) => (
                <li
                  key={username}
                  className={
                    username === currentUser ? "user-item current" : "user-item"
                  }
                >
                  <span className="user-status">●</span>
                  <span className="user-name">{username}</span>
                  {username === currentUser && (
                    <span className="user-badge">(YOU)</span>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default OnlineUsersModal;
