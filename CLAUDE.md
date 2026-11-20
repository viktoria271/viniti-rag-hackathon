# Project Rules (Strict Token Economy)

## Role & Division of Labor
- You are the surgical code executor.
- Research, architecture design, prompt engineering, and large-file analysis are handled externally. Do NOT spend tokens brainstorming or exploring alternatives unless explicitly asked.

## Workflow & Context Discipline
- Execute strictly ONE atomic task at a time (from `TODO.md` or user prompt).
- If `TODO.md` exists: complete ONLY the first unchecked `[ ]` item, mark it `[x]`, and stop immediately.
- Never read entire directories or large files blindly. Use targeted search/line ranges or inspect schemas and first 5 lines only.
- NEVER read raw datasets, `*.pdf`, `*.csv`, `*.xlsx`, `*.parquet`, `*.log`, lockfiles, or large `*.json` files.

## Output & Coding Style
- Be maximally concise. No greetings, no summaries, no "why this works" explanations, no trailing remarks.
- Write clean, minimal, working MVP code. No over-engineering.
- Edit only the specific files required for the current task.
- When fixing errors, state the root cause in 1 line and apply the minimal patch.

## Project Context
- Goal: Scientific PDF parsing pipeline (table/formula/entity extraction -> exact source linking -> unit normalization -> consistency validation -> search/filter UI).
- Stack: [TBD]
- Run / Test commands: [TBD]

## Server Hardware & Resource Limits (STRICT)
- The server has ONLY 1 GB RAM and 10 GB disk space.
- NEVER install heavy libraries (e.g., `pandas`, `torch`, `tensorflow`, `scipy`, local OCR engines like `tesseract`/`easyocr`, or heavy PDF/image suites). Use Python stdlib (`csv`, `json`, `re`, `sqlite3`) and lightweight parsers only.
- Process files strictly ONE by one in streaming/sequential mode; never load the full dataset or multiple PDFs into memory at once.
- Immediately delete any temporary files, caches, and intermediate artifacts after processing.

## Server Hardware & Resource Limits (STRICT)
- The server has ONLY 1 GB RAM and 10 GB disk space.
- NEVER install heavy libraries (e.g., `pandas`, `torch`, `tensorflow`, `scipy`, local OCR engines like `tesseract`/`easyocr`, or heavy PDF/image suites). Use Python stdlib (`csv`, `json`, `re`, `sqlite3`) and lightweight parsers only.
- Process files strictly ONE by one in streaming/sequential mode; never load the full dataset or multiple PDFs into memory at once.
- Immediately delete any temporary files, caches, and intermediate artifacts after processing.
