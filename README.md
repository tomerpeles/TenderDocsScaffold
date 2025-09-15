# Tender RAG Extractor (Hebrew-first)

Solution scaffold for the exercise: page-level tagging → per-parameter prompting → strict JSON output.

## Quickstart
```bash
# (Optional) create a venv
# python -m venv .venv && source .venv/bin/activate  # (Linux/Mac)
# .venv\Scripts\activate                            # (Windows)

pip install -r requirements.txt

# Run with mock LLM (no API key needed)
python main.py --pdf data/tender_sample.pdf --params config/parameters.json --out out --mock

# Run with OpenAI (JSON mode)
# export OPENAI_API_KEY=sk-...  (or set in your shell)
python main.py --pdf data/tender_sample.pdf --params config/parameters.json --out out
```

## What it does
1. Extracts text per page from the PDF (PyMuPDF), with OCR fallback hooks.
2. Tags pages per parameter via hybrid scores (keywords/regex + embeddings when available).
3. Builds a strict Hebrew JSON prompt per parameter and calls the LLM (parallel-ready).
4. Post-processes, normalizes, and computes a 1–5 confidence score.
5. Writes a JSON report and a CSV summary.

## Notes
- If libraries like `pymupdf` or `sentence-transformers` are not installed, the scaffold degrades gracefully and still runs in `--mock` mode.
- You can swap in your preferred LLM provider by editing `src/llm.py`.
