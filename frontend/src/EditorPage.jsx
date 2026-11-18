import Table from "@tiptap/extension-table";
import TableCell from "@tiptap/extension-table-cell";
import TableHeader from "@tiptap/extension-table-header";
import TableRow from "@tiptap/extension-table-row";
import Underline from "@tiptap/extension-underline";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "./api.js";
import { ROLE_LABEL, FILE_TYPE_LABEL } from "./constants.js";
import ShareDialog from "./ShareDialog.jsx";
import Toolbar from "./Toolbar.jsx";

const STATUS_TEXT = {
  saved: "All changes saved",
  unsaved: "Unsaved changes…",
  saving: "Saving…",
  error: "Save failed – will retry on next edit",
};

function DocEditor({ doc }) {
  const canEdit = doc.role === "owner" || doc.role === "edit";
  const supportsTable = !doc.file_extension || doc.file_extension === ".docx";
  const [title, setTitle] = useState(doc.title);
  const [status, setStatus] = useState("saved");
  const [error, setError] = useState("");
  const [sharing, setSharing] = useState(false);

  const pending = useRef({});
  const timer = useRef(null);
  const lastGoodTitle = useRef(doc.title);

  const flush = useCallback(async () => {
    clearTimeout(timer.current);
    const payload = pending.current;
    if (Object.keys(payload).length === 0) return;
    pending.current = {};
    setStatus("saving");
    try {
      const saved = await api.updateDocument(doc.id, payload);
      lastGoodTitle.current = saved.title;
      setError("");
      setStatus(Object.keys(pending.current).length ? "unsaved" : "saved");
    } catch (err) {
      pending.current = { ...payload, ...pending.current };
      setError(err.message);
      setStatus("error");
    }
  }, [doc.id]);

  const queue = useCallback(
    (patch) => {
      pending.current = { ...pending.current, ...patch };
      setStatus("unsaved");
      clearTimeout(timer.current);
      timer.current = setTimeout(flush, 800);
    },
    [flush]
  );

  const extensions = [
    StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
    Underline,
  ];

  // Only add table extensions for native documents or .docx files
  if (supportsTable) {
    extensions.push(
      Table.configure({ resizable: false }),
      TableRow,
      TableHeader,
      TableCell
    );
  }

  const editor = useEditor({
    extensions,
    content: doc.content,
    editable: canEdit,
    onUpdate: ({ editor: ed }) => queue({ content: ed.getHTML() }),
  });

  // Flush pending changes when leaving the page.
  useEffect(() => () => flush(), [flush]);

  // Warn about unsaved changes on tab close.
  useEffect(() => {
    const handler = (e) => {
      if (Object.keys(pending.current).length > 0) {
        e.preventDefault();
        e.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, []);

  function onTitleChange(e) {
    const value = e.target.value;
    setTitle(value);
    if (value.trim()) queue({ title: value.trim() });
  }

  function onTitleBlur() {
    if (!title.trim()) setTitle(lastGoodTitle.current);
    else flush();
  }

  return (
    <main className="container editor-container">
      <div className="editor-top">
        <Link to="/" className="back-link">
          ← All documents
        </Link>
        <div className="editor-meta">
          <span className={`badge ${doc.role}`}>{ROLE_LABEL[doc.role]}</span>
          {doc.role !== "owner" && <span className="muted small-text">by {doc.owner.name}</span>}
          {canEdit && <span className={`status ${status}`}>{STATUS_TEXT[status]}</span>}
          {doc.role === "owner" && (
            <button className="btn" onClick={() => setSharing(true)}>
              Share
            </button>
          )}
        </div>
      </div>

      <input
        className="title-input"
        value={title}
        onChange={onTitleChange}
        onBlur={onTitleBlur}
        disabled={!canEdit}
        maxLength={255}
        aria-label="Document title"
        placeholder="Untitled document"
      />

      {doc.file_extension && (
        <div className="info">
          <span className="badge file-type">{FILE_TYPE_LABEL[doc.file_extension] || doc.file_extension}</span>
          {!supportsTable && " Tables are not supported for this file type"}
        </div>
      )}

      {error && <div className="error">{error}</div>}
      {!canEdit && <div className="info">You have view-only access to this document.</div>}

      {canEdit && <Toolbar editor={editor} supportsTable={supportsTable} />}
      <div className="sheet">
        <EditorContent editor={editor} />
      </div>

      {sharing && <ShareDialog docId={doc.id} onClose={() => setSharing(false)} />}
    </main>
  );
}

export default function EditorPage() {
  const { id } = useParams();
  const [doc, setDoc] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    setDoc(null);
    setError("");
    api
      .getDocument(id)
      .then(setDoc)
      .catch((err) => setError(err.message));
  }, [id]);

  if (error)
    return (
      <main className="container">
        <div className="error">{error}</div>
        <Link to="/">← Back to documents</Link>
      </main>
    );
  if (!doc) return <div className="center-msg">Loading…</div>;
  return <DocEditor key={doc.id} doc={doc} />;
}