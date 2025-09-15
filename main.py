import os, json, argparse, hashlib, time
from tqdm import tqdm
from src.pdf_io import load_pdf_pages
from src.tagging import build_index, tag_pages_for_parameter
from src.prompts import build_prompt_for_param
from src.llm import call_llm_for_param
from src.postprocess import normalize_and_score
from src.report import write_outputs

def hash_obj(o)->str:
    return hashlib.md5(json.dumps(o, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, help="Path to tender PDF")
    parser.add_argument("--params", required=True, help="Path to parameters.json")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--topk", type=int, default=None, help="Override per-param max pages")
    parser.add_argument("--overlap", type=int, default=0, help="Number of words to overlap between text chunks")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM (no API calls)")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    print("Starting…")
    t0 = time.time()

    pages = load_pdf_pages(args.pdf, overlap=args.overlap)
    with open(args.params, "r", encoding="utf-8") as f:
        params = json.load(f)

    embed_index = build_index(pages)  # graceful if embeddings unavailable
    results = []
    traces = []

    for param in tqdm(params, desc="Processing parameters"):
        topk = args.topk or param.get("max_pages", 5)
        tagged = tag_pages_for_parameter(param, pages, embed_index, topk=topk)
        prompt = build_prompt_for_param(param, tagged, pages)

        llm_json = call_llm_for_param(param, prompt, mock=args.mock)
        answer = normalize_and_score(param, llm_json)

        results.append(answer)
        traces.append({
            "parameter": param["key"],
            "tagged_pages": tagged,
            "prompt_chars": len(prompt)
        })

    run_meta = {
        "pdf_path": os.path.abspath(args.pdf),
        "params_hash": hash_obj(params),
        "timestamp": int(time.time()),
        "duration_sec": round(time.time()-t0, 2)
    }

    write_outputs(results, traces, args.out, run_meta)
    print(f"Done. Results written to: {args.out}")

if __name__ == "__main__":
    main()
