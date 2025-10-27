import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const { login, signup } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setFieldErrors({});
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});
    setLoading(true);

    let result;
    if (isLogin) {
      result = await login(formData.username, formData.password);
    } else {
      result = await signup(
        formData.username,
        formData.email,
        formData.password,
        formData.passwordConfirm
      );
    }

    setLoading(false);

    if (result.success) {
      navigate("/");
    } else {
      setError(result.message);
      if (result.errors) {
        setFieldErrors(result.errors);
      }
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setFormData({
      username: "",
      email: "",
      password: "",
      passwordConfirm: "",
    });
    setError("");
    setFieldErrors({});
  };

  return (
    <main>
      <div className="form-container">
        <h1 className="success">{isLogin ? "Login" : "Sign Up"}</h1>

        <div className="auth-tabs">
          <button
            type="button"
            className={isLogin ? "tab-active" : ""}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button
            type="button"
            className={!isLogin ? "tab-active" : ""}
            onClick={() => setIsLogin(false)}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
            {fieldErrors.username && (
              <span className="error">{fieldErrors.username[0]}</span>
            )}
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              {fieldErrors.email && (
                <span className="error">{fieldErrors.email[0]}</span>
              )}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {fieldErrors.password && (
              <span className="error">{fieldErrors.password[0]}</span>
            )}
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="passwordConfirm">Confirm Password</label>
              <input
                type="password"
                id="passwordConfirm"
                name="passwordConfirm"
                value={formData.passwordConfirm}
                onChange={handleChange}
                required
              />
              {fieldErrors.password_confirm && (
                <span className="error">{fieldErrors.password_confirm[0]}</span>
              )}
            </div>
          )}

          {error && <p className="error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : isLogin ? "Login" : "Sign Up"}
          </button>
        </form>

        {isLogin && (
          <p className="auth-link">
            Forgot password? <Link to="/reset-password">Reset it here</Link>
          </p>
        )}

        <p className="auth-link">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button type="button" onClick={toggleMode} className="link-button">
            {isLogin ? "Sign Up" : "Login"}
          </button>
        </p>
      </div>
    </main>
  );
}

export default AuthPage;
