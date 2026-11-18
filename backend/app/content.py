"""HTML sanitising and file-to-HTML import (.txt, .md, .docx)."""
import html
import io
import os

import bleach
import markdown
from docx import Document as DocxDocument
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".txt", ".md", ".docx"}

ALLOWED_TAGS = [
    "p", "br", "hr", "strong", "em", "b", "i", "u", "s", "code", "pre",
    "h1", "h2", "h3", "ul", "ol", "li", "blockquote",
    "table", "thead", "tbody", "tr", "th", "td",
]


def _span_ok(_tag: str, name: str, value: str) -> bool:
    """Only allow small positive integers for colspan/rowspan."""
    return name in ("colspan", "rowspan") and value.isdigit() and 1 <= int(value) <= 50


ALLOWED_ATTRIBUTES = {"td": _span_ok, "th": _span_ok}


class ImportError_(Exception):
    """Raised when an uploaded file cannot be converted."""


def sanitize_html(raw: str) -> str:
    cleaned = bleach.clean(raw, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    return cleaned if cleaned.strip() else "<p></p>"


def _text_to_html(text: str) -> str:
    blocks = [b.strip("\n") for b in text.replace("\r\n", "\n").split("\n\n")]
    paragraphs = [
        "<p>" + html.escape(b).replace("\n", "<br>") + "</p>" for b in blocks if b.strip()
    ]
    return "".join(paragraphs)


def _runs_to_html(paragraph) -> str:
    out = []
    for run in paragraph.runs:
        text = html.escape(run.text).replace("\n", "<br>")
        if not text:
            continue
        if run.bold:
            text = f"<strong>{text}</strong>"
        if run.italic:
            text = f"<em>{text}</em>"
        if run.underline:
            text = f"<u>{text}</u>"
        out.append(text)
    return "".join(out)


def _table_to_html(tbl, doc) -> str:
    """Convert a <w:tbl> element to an HTML table.

    Works on the raw XML so merged cells are not duplicated:
    - horizontal merges become colspan
    - vertical merge continuation cells become empty cells (rowspan is not rebuilt)
    - nested tables inside cells are skipped
    """
    rows_html: list[str] = []
    for tr in tbl.findall(qn("w:tr")):
        cells_html: list[str] = []
        for tc in tr.findall(qn("w:tc")):
            tc_pr = tc.find(qn("w:tcPr"))

            colspan = 1
            continuation = False
            if tc_pr is not None:
                grid_span = tc_pr.find(qn("w:gridSpan"))
                if grid_span is not None:
                    try:
                        colspan = max(1, min(int(grid_span.get(qn("w:val"), "1")), 50))
                    except ValueError:
                        colspan = 1
                v_merge = tc_pr.find(qn("w:vMerge"))
                if v_merge is not None and v_merge.get(qn("w:val")) in (None, "continue"):
                    continuation = True

            paragraphs: list[str] = []
            if not continuation:
                for p in tc.findall(qn("w:p")):
                    inner = _runs_to_html(Paragraph(p, doc))
                    if inner.strip():
                        paragraphs.append(f"<p>{inner}</p>")
            if not paragraphs:
                paragraphs.append("<p></p>")

            attr = f' colspan="{colspan}"' if colspan > 1 else ""
            cells_html.append(f"<td{attr}>{''.join(paragraphs)}</td>")
        if cells_html:
            rows_html.append(f"<tr>{''.join(cells_html)}</tr>")

    if not rows_html:
        return ""
    return f"<table><tbody>{''.join(rows_html)}</tbody></table>"


def _docx_to_html(data: bytes) -> str:
    doc = DocxDocument(io.BytesIO(data))
    parts: list[str] = []
    open_list: str | None = None

    def close_list():
        nonlocal open_list
        if open_list:
            parts.append(f"</{open_list}>")
            open_list = None

    # Walk the body in document order so tables stay between the right paragraphs.
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:tbl"):
            close_list()
            parts.append(_table_to_html(child, doc))
            continue
        if child.tag != qn("w:p"):
            continue

        paragraph = Paragraph(child, doc)
        style = paragraph.style.name if paragraph.style is not None else ""
        inner = _runs_to_html(paragraph)

        list_tag = None
        if style.startswith("List Bullet"):
            list_tag = "ul"
        elif style.startswith("List Number"):
            list_tag = "ol"

        if list_tag:
            if open_list != list_tag:
                close_list()
                parts.append(f"<{list_tag}>")
                open_list = list_tag
            parts.append(f"<li><p>{inner}</p></li>")
            continue

        close_list()
        if not inner.strip():
            continue
        if style == "Title":
            parts.append(f"<h1>{inner}</h1>")
        elif style.startswith("Heading ") and style.split()[-1].isdigit():
            level = min(max(int(style.split()[-1]), 1), 3)
            parts.append(f"<h{level}>{inner}</h{level}>")
        else:
            parts.append(f"<p>{inner}</p>")

    close_list()
    return "".join(parts)


def import_file(filename: str, data: bytes) -> tuple[str, str, str]:
    """Return (title, sanitized_html, file_extension) for an uploaded file."""
    base, ext = os.path.splitext(os.path.basename(filename or ""))
    ext = ext.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ImportError_("Unsupported file type. Use .txt, .md or .docx.")

    try:
        if ext == ".docx":
            raw_html = _docx_to_html(data)
        else:
            text = data.decode("utf-8-sig")
            if ext == ".md":
                # Markdown: convert but strip tables - they don't render well in plain text
                raw_html = markdown.markdown(text, extensions=["extra", "sane_lists"])
                # Remove any table tags from markdown rendering
                raw_html = bleach.clean(
                    raw_html,
                    tags=[t for t in ALLOWED_TAGS if t not in ("table", "thead", "tbody", "tr", "th", "td")],
                    attributes={},
                    strip=True
                )
            else:
                # Plain text - no tables
                raw_html = _text_to_html(text)
    except UnicodeDecodeError:
        raise ImportError_("Text files must be UTF-8 encoded.")
    except Exception:
        raise ImportError_("Could not read this file. It may be corrupted.")

    # Include extension in title for clarity
    title_with_ext = f"{base}{ext}" if base.strip() else f"Imported document{ext}"
    title = title_with_ext.strip()[:255]
    return title, sanitize_html(raw_html), ext