import csv
import json
import re
from pathlib import Path

from .schemas import PaperExtraction

SCHEMA = Path(__file__).resolve().parents[2] / "submission_template" / "schema.json"
BOUNDED = re.compile(r"(?i)(accuracy|precision|recall|f1|exact match|em|hit(?:s)?|mrr|ndcg)(@\d+)?")


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def validate(ex):
    """Deterministic checks; returns extra Issue dicts. Source rows are never removed."""
    out = []

    def add(rows, name, desc, r):
        out.append({"record_ids": ";".join(rows), "check_name": name, "description": desc,
                    "source_page": r.source_page, "source_fragment": r.source_fragment})

    for r in ex.results:
        v = _num(r.metric_value)
        name = (r.metric_name or "").strip()
        if v is not None and BOUNDED.fullmatch(name):
            lim = 1 if r.metric_unit == "fraction" else 100 if r.metric_unit == "%" else None
            if lim and not 0 <= v <= lim:
                add([r.result_id], "metric_scale", f"{name}={r.metric_value} outside [0,{lim}] for unit {r.metric_unit}", r)
            elif lim == 100 and v <= 1 and v != 0 and "%" not in (r.raw_value or "") + (r.raw_unit or ""):
                add([r.result_id], "metric_scale", f"{name}={r.metric_value} unit '%' but raw looks like a fraction", r)
        if re.search(r"@\d+$", name) and not r.metric_k:
            add([r.result_id], "metric_k", f"{name} has no metric_k", r)
        ru = (r.raw_unit or "").lower()
        if "point" in ru and r.metric_unit == "%":
            add([r.result_id], "normalization", "percentage points recorded as %", r)
    return out


def _s(v):
    return "" if v is None else ("true" if v is True else "false" if v is False else str(v))


def export(cache_dir, out_dir, only=None):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    tables = schema["tables"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = {t: open(out / f"{t}.csv", "w", encoding="utf-8", newline="") for t in tables}
    writers = {t: csv.DictWriter(files[t], fieldnames=c) for t, c in tables.items()}
    for w in writers.values():
        w.writeheader()
    try:
        for cp in sorted(Path(cache_dir).glob("*.json")):
            pid = cp.stem
            if only and pid not in only:
                continue
            ex = PaperExtraction.model_validate_json(cp.read_text(encoding="utf-8"))
            writers["publications"].writerow({"publication_id": pid, **{k: _s(v) for k, v in ex.publication.model_dump().items()}})
            if not ex.publication.in_scope:
                continue
            for t in ("configurations", "datasets", "tasks", "experiments", "results", "issues"):
                for item in getattr(ex, t):
                    writers[t].writerow({"publication_id": pid, **{k: _s(v) for k, v in item.model_dump().items()}})
            for n, d in enumerate(validate(ex), 1):
                writers["issues"].writerow({"publication_id": pid, "issue_id": f"V{n:03d}", **{k: _s(v) for k, v in d.items()}})
    finally:
        for f in files.values():
            f.close()
