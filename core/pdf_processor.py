from pathlib import Path

import pymupdf

MIN_CHARS_PER_PAGE = 30


def process_pdf(path):
    """Return {'doc_id','n_pages','is_scan','text'}; text has '--- PAGE N ---' markers (N from 1)."""
    path = Path(path)
    parts, chars = [], 0
    with pymupdf.open(path) as doc:
        n = len(doc)
        for i, page in enumerate(doc, 1):
            t = page.get_text() or ""
            chars += len(t.strip())
            parts.append(f"--- PAGE {i} ---\n{t}")
    is_scan = n == 0 or chars / n < MIN_CHARS_PER_PAGE
    return {
        "doc_id": path.stem,
        "path": path,
        "n_pages": n,
        "is_scan": is_scan,
        "text": "" if is_scan else "\n".join(parts),
    }
