import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
RETRY_CODES = {429, 500, 503, 504}


class LLMClient:
    def __init__(self, cache_dir="cache", model=DEFAULT_MODEL, retries=5):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.cache_dir = Path(cache_dir)
        self.model = model
        self.retries = retries

    def cache_path(self, doc_id):
        return self.cache_dir / f"{doc_id}.json"

    def _call(self, contents, system, schema):
        cfg = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0,
        )
        for attempt in range(self.retries):
            try:
                return self.client.models.generate_content(
                    model=self.model, contents=contents, config=cfg
                ).text
            except errors.APIError as e:
                if e.code not in RETRY_CODES or attempt == self.retries - 1:
                    raise
                time.sleep(min(60, 5 * 2**attempt))

    def extract(self, doc, system, user_prompt, schema, force=False):
        """Return raw JSON text for a doc (from cache unless force). doc: core.pdf_processor result."""
        cp = self.cache_path(doc["doc_id"])
        if cp.exists() and not force:
            return cp.read_text(encoding="utf-8")
        uploaded = None
        try:
            if doc["is_scan"]:
                uploaded = self.client.files.upload(file=str(doc["path"]))
                contents = [uploaded, user_prompt]
            else:
                contents = [user_prompt + "\n\n" + doc["text"]]
            raw = self._call(contents, system, schema)
        finally:
            if uploaded is not None:
                try:
                    self.client.files.delete(name=uploaded.name)
                except Exception:
                    pass
        json.loads(raw)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cp.write_text(raw, encoding="utf-8")
        return raw
