import os, json, random

def _mock_answer(param_key, prompt):
    # Very simple mock for offline runs
    if "idea_author" in param_key:
        return {"parameter": param_key, "answer": "אצמנ אל", "details": "", "source": [], "confidence": 1}
    # fabricate something deterministic-ish
    base = {
        "parameter": param_key,
        "answer": "דוגמה",
        "details": "תשובה לדוגמה במצב הדמיה (mock).",
        "source": [{"page": 1, "snippet": "…"}],
        "confidence": 2
    }
    return base

def call_llm_for_param(param, prompt, mock=False):
    if mock or not os.getenv("OPENAI_API_KEY"):
        return _mock_answer(param.get("key",""), prompt)

    try:
        from openai import OpenAI
        client = OpenAI()
        # JSON-mode style; adjust to your chosen model
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role":"system","content":"החזר JSON בלבד."},
                {"role":"user","content":prompt}
            ],
            temperature=0.2
        )
        content = resp.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        # fallback to mock if API fails
        return _mock_answer(param.get("key",""), prompt)
