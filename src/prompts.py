import json

def build_prompt_for_param(param, tagged_pages, pages):
    """
    Returns a Hebrew prompt string that includes only the tagged pages' text.
    """
    header = (
        "אתה ממלא תפקיד של 'מחלץ נתונים ממכרזים'. "
        "החזר אך ורק JSON תקין בהתאם לסכימה. "
        "source= המיקום במסמך שממנו שאבת את התשובה (מספר עמוד ונוסף אחד מאלה: מספר פיסקה,כותרת עליונה, כותרת תחתונה). לדוגמה : עמוד 1, פסקה ראשונה."
        "details = פירוט נוסף, ניסוח מורחב או פרשנות. הרחב והסבר למה נבחרה התשובה לפרמטר."
        "אם אין מידע – החזר answer='לא נמצא', והשאר details ו-source ריקים.\n"
        ""
        ""
    )
    body = []
    for p in pages:
        if p["page_no"] in tagged_pages:
            snippet = p["text"]
            # keep prompt reasonable
            snippet = snippet[:5000]
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
        f"תיאור:   {param.get('description_he','')}. "
        "JSON בלבד, ללא טקסט חופשי נוסף."
    )

    prompt = header + body_text + "\n\n" + instruction + "\n" + json.dumps(schema, ensure_ascii=False)
    return prompt
