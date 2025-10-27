import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axiosInstance from "../utils/axios-config";

function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate();

  const step = token ? "reset" : "request";
  const [email, setEmail] = useState("");
  const [formData, setFormData] = useState({
    newPassword: "",
    passwordConfirm: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await axiosInstance.post(
        "/api/auth/request-password-reset/",
        {
          email,
        }
      );
      setMessage(response.data.message);
      setEmail("");
    } catch (err) {
      setError(err.response?.data?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await axiosInstance.post("/api/auth/reset-password/", {
        token,
        new_password: formData.newPassword,
        password_confirm: formData.passwordConfirm,
      });
      setMessage(response.data.message);
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.message || "Reset failed");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError("");
  };

  return (
    <main>
      <div className="form-container">
        {step === "request" ? (
          <>
            <h1 className="success">Reset Password</h1>
            <p>Enter your email to receive a reset link</p>

            <form onSubmit={handleRequestReset}>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              {message && <p className="success">{message}</p>}
              {error && <p className="error">{error}</p>}

              <button type="submit" disabled={loading}>
                {loading ? "Sending..." : "Send Reset Link"}
              </button>
            </form>

            <p className="auth-link">
              Remember your password? <a href="/login">Login</a>
            </p>
          </>
        ) : (
          <>
            <h1 className="success">Set New Password</h1>
            <p>Enter your new password</p>

            <form onSubmit={handleResetPassword}>
              <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                  type="password"
                  id="newPassword"
                  name="newPassword"
                  value={formData.newPassword}
                  onChange={handleChange}
                  required
                  minLength={8}
                />
              </div>

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
              </div>

              {message && <p className="success">{message}</p>}
              {error && <p className="error">{error}</p>}

              <button type="submit" disabled={loading}>
                {loading ? "Resetting..." : "Reset Password"}
              </button>
            </form>
          </>
        )}
      </div>
    </main>
  );
}

export default ResetPasswordPage;
