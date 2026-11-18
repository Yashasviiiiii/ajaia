function Btn({ active, disabled, onClick, title, children }) {
  return (
    <button
      type="button"
      title={title}
      disabled={disabled}
      className={`tb-btn ${active ? "active" : ""}`}
      onMouseDown={(e) => e.preventDefault()} // keep editor selection
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default function Toolbar({ editor, supportsTable = true }) {
  if (!editor) return null;

  const headingValue = [1, 2, 3].find((l) => editor.isActive("heading", { level: l })) ?? 0;
  const inTable = editor.isActive("table");

  function onStyleChange(e) {
    const level = Number(e.target.value);
    const chain = editor.chain().focus();
    if (level === 0) chain.setParagraph().run();
    else chain.setHeading({ level }).run();
  }

  const run = (cmd) => editor.chain().focus()[cmd]().run();

  return (
    <>
      <div className="toolbar">
        <select value={headingValue} onChange={onStyleChange} title="Text style">
          <option value={0}>Normal text</option>
          <option value={1}>Heading 1</option>
          <option value={2}>Heading 2</option>
          <option value={3}>Heading 3</option>
        </select>
        <span className="sep" />
        <Btn
          title="Bold (Ctrl+B)"
          active={editor.isActive("bold")}
          onClick={() => editor.chain().focus().toggleBold().run()}
        >
          <b>B</b>
        </Btn>
        <Btn
          title="Italic (Ctrl+I)"
          active={editor.isActive("italic")}
          onClick={() => editor.chain().focus().toggleItalic().run()}
        >
          <i>I</i>
        </Btn>
        <Btn
          title="Underline (Ctrl+U)"
          active={editor.isActive("underline")}
          onClick={() => editor.chain().focus().toggleUnderline().run()}
        >
          <u>U</u>
        </Btn>
        <span className="sep" />
        <Btn
          title="Bulleted list"
          active={editor.isActive("bulletList")}
          onClick={() => editor.chain().focus().toggleBulletList().run()}
        >
          • List
        </Btn>
        <Btn
          title="Numbered list"
          active={editor.isActive("orderedList")}
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
        >
          1. List
        </Btn>
        {supportsTable && (
          <>
            <span className="sep" />
            <Btn
              title="Insert 3×3 table"
              disabled={inTable}
              onClick={() =>
                editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()
              }
            >
              ▦ Table
            </Btn>
          </>
        )}
        <span className="sep" />
        <Btn
          title="Undo"
          disabled={!editor.can().undo()}
          onClick={() => editor.chain().focus().undo().run()}
        >
          ↶
        </Btn>
        <Btn
          title="Redo"
          disabled={!editor.can().redo()}
          onClick={() => editor.chain().focus().redo().run()}
        >
          ↷
        </Btn>
      </div>

      {inTable && supportsTable && (
        <div className="toolbar toolbar-table">
          <span className="muted small-text">Table:</span>
          <Btn title="Add row above" onClick={() => run("addRowBefore")}>
            + Row above
          </Btn>
          <Btn title="Add row below" onClick={() => run("addRowAfter")}>
            + Row below
          </Btn>
          <Btn
            title="Delete row"
            disabled={!editor.can().deleteRow()}
            onClick={() => run("deleteRow")}
          >
            − Row
          </Btn>
          <span className="sep" />
          <Btn title="Add column left" onClick={() => run("addColumnBefore")}>
            + Col left
          </Btn>
          <Btn title="Add column right" onClick={() => run("addColumnAfter")}>
            + Col right
          </Btn>
          <Btn
            title="Delete column"
            disabled={!editor.can().deleteColumn()}
            onClick={() => run("deleteColumn")}
          >
            − Col
          </Btn>
          <span className="sep" />
          <Btn
            title="Merge selected cells, or split a merged cell"
            disabled={!editor.can().mergeOrSplit()}
            onClick={() => run("mergeOrSplit")}
          >
            Merge/Split
          </Btn>
          <Btn title="Toggle header row" onClick={() => run("toggleHeaderRow")}>
            Header row
          </Btn>
          <span className="sep" />
          <Btn title="Delete table" onClick={() => run("deleteTable")}>
            🗑 Table
          </Btn>
        </div>
      )}
    </>
  );
}