import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "./api.js";
import { ROLE_LABEL, FILE_TYPE_LABEL } from "./constants.js";

function DocList({ docs, emptyText, onDelete, showOwner }) {
  if (docs.length === 0) return <p className="muted">{emptyText}</p>;
  return (
    <ul className="doc-list">
      {docs.map((d) => (
        <li key={d.id} className="doc-row">
          <Link to={`/docs/${d.id}`} className="doc-main">
            <span className="doc-title">
              {d.title}
              {d.file_extension && (
                <span className="badge file-type">{FILE_TYPE_LABEL[d.file_extension] || d.file_extension}</span>
              )}
            </span>
            <span className="muted small-text">
              {showOwner && `Shared by ${d.owner.name} · `}
              Updated {new Date(d.updated_at).toLocaleString()}
            </span>
          </Link>
          <span className={`badge ${d.role}`}>{ROLE_LABEL[d.role]}</span>
          {onDelete && (
            <button className="btn small danger" onClick={() => onDelete(d)}>
              Delete
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}

export default function Dashboard() {
  const navigate = useNavigate();
  const fileRef = useRef(null);
  const [data, setData] = useState({ owned: [], shared: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [showNewDocDialog, setShowNewDocDialog] = useState(false);

  const load = useCallback(async () => {
    try {
      setData(await api.listDocuments());
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function createDoc(fileExtension = null) {
    setBusy(true);
    setShowNewDocDialog(false);
    try {
      const doc = await api.createDocument({ file_extension: fileExtension });
      navigate(`/docs/${doc.id}`);
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  async function onFileChosen(e) {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const doc = await api.importDocument(form);
      
      // Check if title was auto-renamed (has suffix like " (2)")
      const originalName = file.name;
      if (doc.title !== originalName && doc.title.match(/\s\(\d+\)\.\w+$/)) {
        setError(`File imported as "${doc.title}" (a file with that name already exists)`);
      }
      
      navigate(`/docs/${doc.id}`);
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  async function removeDoc(doc) {
    if (!window.confirm(`Delete "${doc.title}"? This also removes it for anyone it is shared with.`))
      return;
    try {
      await api.deleteDocument(doc.id);
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="container">
      <div className="toolbar-row">
        <h1>Documents</h1>
        <div className="actions">
          <input
            ref={fileRef}
            type="file"
            accept=".txt,.md,.docx"
            hidden
            onChange={onFileChosen}
          />
          <button className="btn" disabled={busy} onClick={() => fileRef.current?.click()}>
            Upload file
          </button>
          <button className="btn primary" disabled={busy} onClick={() => setShowNewDocDialog(true)}>
            + New document
          </button>
        </div>
      </div>
      <p className="muted small-text">
        Upload turns a file into a new editable document. Supported: .txt, .md, .docx (max 5 MB).
        For .docx, headings, bold/italic/underline, lists and tables are preserved.
        For .txt and .md, tables are not supported.
      </p>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <p className="muted">Loading…</p>
      ) : (
        <>
          <section>
            <h2>My documents</h2>
            <DocList
              docs={data.owned}
              emptyText="You haven't created any documents yet."
              onDelete={removeDoc}
            />
          </section>
          <section>
            <h2>Shared with me</h2>
            <DocList docs={data.shared} emptyText="Nothing has been shared with you." showOwner />
          </section>
        </>
      )}

      {showNewDocDialog && (
        <div className="modal-backdrop" onClick={() => setShowNewDocDialog(false)}>
          <div className="card modal" onClick={(e) => e.stopPropagation()}>
            <h2>Create New Document</h2>
            <p className="muted small-text">Choose the type of document you want to create:</p>
            
            <div className="doc-type-grid">
              <button 
                className="doc-type-card" 
                onClick={() => createDoc(".docx")}
                disabled={busy}
              >
                <div className="doc-type-icon">📄</div>
                <div className="doc-type-title">Word Document (.docx)</div>
                <div className="doc-type-desc">Full-featured document with tables, formatting, and all editing tools</div>
                <div className="doc-type-features">
                  <span className="feature-tag">✓ Tables</span>
                  <span className="feature-tag">✓ All formatting</span>
                </div>
              </button>

              <button 
                className="doc-type-card" 
                onClick={() => createDoc(".md")}
                disabled={busy}
              >
                <div className="doc-type-icon">📝</div>
                <div className="doc-type-title">Markdown Document (.md)</div>
                <div className="doc-type-desc">Simple formatting for documentation and notes</div>
                <div className="doc-type-features">
                  <span className="feature-tag">✗ No tables</span>
                  <span className="feature-tag">✓ Basic formatting</span>
                </div>
              </button>

              <button 
                className="doc-type-card" 
                onClick={() => createDoc(".txt")}
                disabled={busy}
              >
                <div className="doc-type-icon">📃</div>
                <div className="doc-type-title">Plain Text Document (.txt)</div>
                <div className="doc-type-desc">Basic text with minimal formatting</div>
                <div className="doc-type-features">
                  <span className="feature-tag">✗ No tables</span>
                  <span className="feature-tag">✓ Simple text</span>
                </div>
              </button>
            </div>

            <button className="btn" onClick={() => setShowNewDocDialog(false)} style={{ marginTop: '1rem' }}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </main>
  );
}