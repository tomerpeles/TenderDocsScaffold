import json

def build_prompt_for_param(param, tagged_pages, pages):
    """
    Returns a Hebrew prompt string that includes only the tagged pages' text.
    """
    # Build document content blocks
    content_blocks = []
    for p in pages:
        if p["page_no"] in tagged_pages:
            snippet = p["text"][:10000]  # keep prompt reasonable
            content_blocks.append(f"### עמוד {p['page_no']}\n```\n{snippet}\n```")

    document_content = "\n\n".join(content_blocks) if content_blocks else "### אין עמודים רלוונטיים\n```\nלא נמצאו עמודים רלוונטיים\n```"

    schema = {
        "parameter": param.get("key"),
        "answer": "",
        "details": "",
        "source": [],
        "confidence": 1
    }

    prompt = f"""# מחלץ נתונים ממכרזים

## הוראות
אתה ממלא תפקיד של 'מחלץ נתונים ממכרזים'.
- החזר **אך ורק JSON תקין** בהתאם לסכימה המצורפת
- אם אין מידע – החזר answer='לא נמצא', והשאר details ו-source ריקים
- source: המיקום בעמוד ממנו נלקח המידע. אם לא מצאת מידע אז השאר ערך ריק

## תוכן המסמך
{document_content}

## משימה
הפק תשובה עבור הפרמטר: **{param.get('label_he','')}** ({param.get('key','')})

## סכימת JSON נדרשת
```json
{json.dumps(schema, ensure_ascii=False, indent=2)}
```

**החזר JSON בלבד, ללא טקסט חופשי נוסף.**"""

    return prompt
