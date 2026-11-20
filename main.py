import argparse
from pathlib import Path

from plugins.rag.exporter import export


def main():
    ap = argparse.ArgumentParser(description="RAG PDF extraction pipeline")
    ap.add_argument("--input", default="dev", help="folder with PDFs")
    ap.add_argument("--output", default="out_dev", help="folder for 7 CSV")
    ap.add_argument("--only", nargs="*", help="doc ids, e.g. D001 D002")
    ap.add_argument("--force", action="store_true", help="ignore cache")
    ap.add_argument("--rebuild-csv-only", action="store_true", help="rebuild CSV from cache/ without API calls")
    ap.add_argument("--cache", default="cache")
    a = ap.parse_args()

    if not a.rebuild_csv_only:
        from core.llm_client import LLMClient
        from core.pdf_processor import process_pdf
        from plugins.rag.prompts import SYSTEM_PROMPT, USER_PROMPT, USER_PROMPT_SCAN
        from plugins.rag.schemas import PaperExtraction

        client = LLMClient(cache_dir=a.cache)
        for pdf in sorted(Path(a.input).glob("*.pdf")):
            if a.only and pdf.stem not in a.only:
                continue
            if client.cache_path(pdf.stem).exists() and not a.force:
                print(f"skip {pdf.stem} (cached)")
                continue
            doc = process_pdf(pdf)
            print(f"{pdf.stem}: pages={doc['n_pages']} scan={doc['is_scan']}")
            try:
                client.extract(doc, SYSTEM_PROMPT, USER_PROMPT_SCAN if doc["is_scan"] else USER_PROMPT, PaperExtraction, a.force)
            except Exception as e:
                print(f"FAIL {pdf.stem}: {e}")
    export(a.cache, a.output, set(a.only) if a.only else None)
    print(f"CSV written to {a.output}")


if __name__ == "__main__":
    main()
