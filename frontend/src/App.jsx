import { Link, Navigate, Outlet, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth.jsx";
import Dashboard from "./Dashboard.jsx";
import EditorPage from "./EditorPage.jsx";
import Login from "./Login.jsx";

function Layout() {
  const { user, loading, logout } = useAuth();
  if (loading) return <div className="center-msg">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <>
      <header className="app-header">
        <Link to="/" className="brand">
          📄 Docs
        </Link>
        <div className="header-right">
          <span className="user-chip">
            {user.name} <span className="session-badge">This Tab</span>
          </span>
          <button className="btn" onClick={logout}>
            Sign out
          </button>
        </div>
      </header>
      <Outlet />
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/docs/:id" element={<EditorPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}