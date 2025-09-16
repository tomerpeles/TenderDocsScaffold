import re, math

# Global cache for the sentence transformer model
_sentence_model = None

def _get_sentence_model():
    """Get or create the sentence transformer model (singleton pattern)"""
    global _sentence_model
    if _sentence_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sentence_model = SentenceTransformer("intfloat/multilingual-e5-base")
        except Exception:
            return None
    return _sentence_model

def _lower_he(text):
    return text.lower()

def keyword_score(text, keywords, regexes):
    score = 0.0
    t = _lower_he(text)
    for kw in (keywords or []):
        score += t.count(kw.lower()) * 1.0
    for rx in (regexes or []):
        try:
            score += len(re.findall(rx, t)) * 2.0
        except re.error:
            pass
    return score

def try_embed_pages(pages):
    """
    Optional embeddings. If sentence-transformers not available, returns None.
    """
    model = _get_sentence_model()
    if model is None:
        return None

    try:
        texts = [p["text"][:2000] for p in pages]
        embs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return {"embs": embs}
    except Exception:
        return None

def build_index(pages):
    vec = try_embed_pages(pages)
    return {"vec": vec}

def semantic_score(param, page, index):
    vec = index.get("vec")
    if not vec:
        return 0.0

    model = _get_sentence_model()
    if model is None:
        return 0.0

    # Build a tiny "profile" sentence for the parameter
    profile = " ".join(param.get("keywords", []) or [])
    if not profile.strip():
        profile = param.get("label_he", param.get("key", ""))

    # One-off encode profile each call (could be cached if needed)
    try:
        import numpy as np
        emb_p = model.encode([profile], normalize_embeddings=True)[0]
    except Exception:
        return 0.0

    # cosine sim with the page embedding
    # find index of page
    # (we assume stable order; a robust impl would map ids)
    i = page["page_no"] - 1
    emb_page = vec["embs"][i]
    return float(np.dot(emb_p, emb_page))

def tag_pages_for_parameter(param, pages, index, topk=6):
    scored = []
    for p in pages:
        ks = keyword_score(p["text"], param.get("keywords", []), param.get("regex", []))
        ss = semantic_score(param, p, index)
        hybrid = 0.6*ss + 0.4*ks
        scored.append((p["page_no"], hybrid, ks, ss))
    # sort by hybrid desc, keep topk > 0 and positive scores
    scored.sort(key=lambda x: x[1], reverse=True)
    tagged = [pg for pg,hy,ks,ss in scored if hy>0][:topk]
    return tagged
