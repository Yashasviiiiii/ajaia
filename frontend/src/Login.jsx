import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "./auth.jsx";

const DEMO_USERS = [
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob", email: "bob@example.com" },
  { name: "Carol", email: "carol@example.com" },
];

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("alice@example.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email, password);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <form className="card login-card" onSubmit={onSubmit}>
        <h1>Sign in to Docs</h1>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {error && <div className="error">{error}</div>}
        <button className="btn primary" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
        <div className="demo">
          <span>Demo accounts (password: password123)</span>
          <div className="demo-buttons">
            {DEMO_USERS.map((u) => (
              <button
                key={u.email}
                type="button"
                className="btn small"
                onClick={() => {
                  setEmail(u.email);
                  setPassword("password123");
                }}
              >
                {u.name}
              </button>
            ))}
          </div>
          <p style={{ fontSize: '0.75rem', marginTop: '0.5rem', opacity: 0.8 }}>
            💡 Tip: Open multiple tabs to login as different users simultaneously
          </p>
        </div>
      </form>
    </div>
  );
}