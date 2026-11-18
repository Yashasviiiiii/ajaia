import { useEffect, useState } from "react";
import { api } from "./api.js";

export default function ShareDialog({ docId, onClose }) {
  const [users, setUsers] = useState([]);
  const [shares, setShares] = useState([]);
  const [email, setEmail] = useState("");
  const [permission, setPermission] = useState("view");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      const [u, s] = await Promise.all([api.users(), api.listShares(docId)]);
      setUsers(u);
      setShares(s);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [docId]);

  const sharedIds = new Set(shares.map((s) => s.user.id));
  const candidates = users.filter((u) => !sharedIds.has(u.id));

  async function addShare(e) {
    e.preventDefault();
    if (!email) return;
    setBusy(true);
    setError("");
    try {
      await api.share(docId, email, permission);
      setEmail("");
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function changePermission(s, next) {
    setError("");
    try {
      await api.share(docId, s.user.email, next);
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function revoke(s) {
    setError("");
    try {
      await api.revokeShare(docId, s.user.id);
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal card" onClick={(e) => e.stopPropagation()}>
        <div className="toolbar-row">
          <h2>Share document</h2>
          <button className="btn small" onClick={onClose}>
            Close
          </button>
        </div>

        <form className="share-form" onSubmit={addShare}>
          <select value={email} onChange={(e) => setEmail(e.target.value)} required>
            <option value="">Select a person…</option>
            {candidates.map((u) => (
              <option key={u.id} value={u.email}>
                {u.name} ({u.email})
              </option>
            ))}
          </select>
          <select value={permission} onChange={(e) => setPermission(e.target.value)}>
            <option value="view">Can view</option>
            <option value="edit">Can edit</option>
          </select>
          <button className="btn primary" disabled={busy || !email}>
            Share
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        <h3>People with access</h3>
        {shares.length === 0 ? (
          <p className="muted">Only you can see this document.</p>
        ) : (
          <ul className="share-list">
            {shares.map((s) => (
              <li key={s.user.id}>
                <span>
                  {s.user.name} <span className="muted small-text">{s.user.email}</span>
                </span>
                <span className="share-actions">
                  <select
                    value={s.permission}
                    onChange={(e) => changePermission(s, e.target.value)}
                  >
                    <option value="view">Can view</option>
                    <option value="edit">Can edit</option>
                  </select>
                  <button className="btn small danger" onClick={() => revoke(s)}>
                    Remove
                  </button>
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}