"""Compare an output folder with dev_gold. Usage: python scripts/evaluate.py [out_dir] [gold_dir]"""
import csv
import sys
from collections import Counter
from pathlib import Path

TABLES = ["publications", "configurations", "datasets", "tasks", "experiments", "results", "issues"]


def load(d, t):
    p = Path(d) / f"{t}.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(s):
    return " ".join((s or "").lower().split())


def num(s):
    try:
        return f"{float(s):.6g}"
    except (TypeError, ValueError):
        return ""


def prf(pred, gold):
    tp = sum((pred & gold).values())
    p = tp / max(sum(pred.values()), 1)
    r = tp / max(sum(gold.values()), 1)
    return p, r, 2 * p * r / (p + r) if p + r else 0.0


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out_dev"
    gold = sys.argv[2] if len(sys.argv) > 2 else "dev_gold"
    O = {t: load(out, t) for t in TABLES}
    G = {t: load(gold, t) for t in TABLES}

    pub = {r["publication_id"]: r["in_scope"] for r in O["publications"]}
    gp = {r["publication_id"]: r["in_scope"] for r in G["publications"]}
    common = [k for k in gp if k in pub]
    ok = sum(pub[k] == gp[k] for k in common)
    print(f"== publications: scope accuracy {ok}/{len(gp)} (missing in output: {len(gp) - len(common)})")
    for k in common:
        if pub[k] != gp[k]:
            print(f"   {k}: out={pub[k]} gold={gp[k]}")

    print("== row counts (out / gold)")
    for t in TABLES:
        print(f"   {t:15} {len(O[t]):5} / {len(G[t]):5}")

    def ctr(rows, f):
        return Counter(x for x in map(f, rows) if x)

    sets = {
        "datasets": ("datasets", lambda r: (r["publication_id"], norm(r["dataset_name"])) if r["dataset_name"] else None),
        "models": ("configurations", lambda r: (r["publication_id"], norm(r["generator_model"])) if r["generator_model"] else None),
        "metric names": ("results", lambda r: (r["publication_id"], norm(r["metric_name"]), r["metric_k"]) if r["metric_name"] else None),
        "metric values": ("results", lambda r: (r["publication_id"], norm(r["metric_name"]), r["metric_k"], num(r["metric_value"])) if num(r["metric_value"]) else None),
    }
    print("== P / R / F1")
    for name, (t, f) in sets.items():
        p, r, f1 = prf(ctr(O[t], f), ctr(G[t], f))
        print(f"   {name:14} P={p:.3f} R={r:.3f} F1={f1:.3f}")

    f = sets["metric values"][1]
    po, pg = ctr(O["results"], f), ctr(G["results"], f)
    diffs = [("missing", k, n) for k, n in (pg - po).items()] + [("extra", k, n) for k, n in (po - pg).items()]
    diffs.sort(key=lambda d: -d[2])
    print("== top-5 discrepancies (results)")
    for kind, k, n in diffs[:5]:
        print(f"   {kind} x{n}: {k}")


if __name__ == "__main__":
    main()
