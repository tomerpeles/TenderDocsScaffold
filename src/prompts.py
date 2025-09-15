import json

def build_prompt_for_param(param, tagged_pages, pages):
    """
    Returns a Hebrew prompt string that includes only the tagged pages' text.
    """
    header = (
        "אתה ממלא תפקיד של 'מחלץ נתונים ממכרזים'. "
        "החזר אך ורק JSON תקין בהתאם לסכימה. "
        "אם אין מידע – החזר answer='אצמנ אל', והשאר details ו-source ריקים.\n"
    )
    body = []
    for p in pages:
        if p["page_no"] in tagged_pages:
            snippet = p["text"]
            # keep prompt reasonable
            snippet = snippet[:3000]
            body.append(f"[PAGE {p['page_no']}]\n{snippet}")
    body_text = "\n\n".join(body) if body else "[אין עמודים רלוונטיים]"

    schema = {
        "parameter": param.get("key"),
        "answer": "",
        "details": "",
        "source": [],
        "confidence": 1
    }

    instruction = (
        f"הפק תשובה עבור הפרמטר: {param.get('label_he','')} ({param.get('key','')}). "
        "JSON בלבד, ללא טקסט חופשי נוסף."
    )

    prompt = header + body_text + "\n\n" + instruction + "\n" + json.dumps(schema, ensure_ascii=False)
    return prompt
