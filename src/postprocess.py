import re, json

def normalize_money(text):
    if not isinstance(text, str):
        return text
    t = text.replace(",", "")
    m = re.findall(r"(\d+(?:\.\d+)?)", t)
    return m[0] if m else text

def normalize_period(text):
    if not isinstance(text, str):
        return text
    # keep as-is; you can add month/year mapping here
    return text

def compute_confidence(raw):
    # Simple heuristic
    c = 1
    ans = ''
    ans = str((raw or {}).get("answer","")).strip()
    # if isinstance((raw or {}).get("answer",""), dict) :
    #     ans = str((raw or {}).get("answer","")).strip()
    # else:
    #     ans = (raw or {}).get("answer","").strip()
    src = (raw or {}).get("source","")
    if ans and ans != "לא נמצא":
        c += 1
    if isinstance(src, list) and len(src) >= 1:
        c += 1
    if len(ans) >= 2:
        c += 1
    return min(c,5)

def normalize_and_score(param, llm_json):
    out = dict(llm_json)
    ptype = param.get("type")
    if ptype == "money":
        out["answer"] = normalize_money(out.get("answer",""))
    elif ptype == "period":
        out["answer"] = normalize_period(out.get("answer",""))
    out["confidence"] = compute_confidence(out)
    # ensure keys exist
    out.setdefault("details","")
    out.setdefault("source",[])
    out.setdefault("parameter", param.get("key",""))
    # missing policy
    if (not out.get("answer")) and param.get("if_missing"):
        out["answer"] = param["if_missing"]
    return out
