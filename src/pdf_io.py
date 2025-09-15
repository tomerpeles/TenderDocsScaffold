import os

def load_pdf_pages(pdf_path, overlap=0):
    """
    Returns a list of dicts: [{ "page_no": 1, "text": "..." }, ...]
    Gracefully degrades if PyMuPDF is not available.

    Args:
        pdf_path: Path to the PDF file
        overlap: Number of words to overlap between text chunks (default: 0)
    """
    pages = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)

        # First pass: extract all page texts
        all_page_texts = []
        for page in doc:
            text = page.get_text("text")
            if not text or len(text.strip()) < 10:
                # OCR hook could go here if needed
                text = ""
            all_page_texts.append(text)

        # Second pass: apply overlap
        for i, text in enumerate(all_page_texts):
            final_text = text

            # Add overlap from next page if it exists and overlap > 0
            if overlap > 0 and i + 1 < len(all_page_texts):
                next_page_text = all_page_texts[i + 1]
                next_words = next_page_text.split()
                overlap_words = next_words[:min(overlap, len(next_words))]
                if overlap_words:
                    final_text += " " + " ".join(overlap_words)

            pages.append({"page_no": i+1, "text": final_text})

        doc.close()
    except Exception as e:
        # Minimal fallback without external libs: read as binary placeholder
        # (For real use, please install pymupdf)
        pages = [{"page_no": 1, "text": f"[PyMuPDF not available] {os.path.basename(pdf_path)}"}]
    return pages
