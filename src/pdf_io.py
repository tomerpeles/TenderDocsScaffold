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
        all_text = ""
        page_texts = []

        # First pass: extract all text from pages
        for i, page in enumerate(doc):
            text = page.get_text("text")
            if not text or len(text.strip()) < 10:
                # OCR hook could go here if needed
                text = ""
            page_texts.append({"page_no": i+1, "text": text})
            all_text += text + " "

        doc.close()

        # If overlap is 0, return original page-based structure
        if overlap == 0:
            return page_texts

        # Apply overlap by appending words from next page to current page
        for i in range(len(page_texts)):
            current_page = page_texts[i]

            # If there's a next page, append overlap words from it
            if i + 1 < len(page_texts):
                next_page_text = page_texts[i + 1]["text"]
                next_page_words = next_page_text.split()

                # Take up to 'overlap' words from next page
                overlap_words = next_page_words[:min(overlap, len(next_page_words))]

                if overlap_words:
                    current_page["text"] += " " + " ".join(overlap_words)

        return page_texts

    except Exception as e:
        # Minimal fallback without external libs: read as binary placeholder
        # (For real use, please install pymupdf)
        pages = [{"page_no": 1, "text": f"[PyMuPDF not available] {os.path.basename(pdf_path)}"}]
    return pages
