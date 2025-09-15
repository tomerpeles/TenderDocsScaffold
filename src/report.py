import os, json, csv

def write_outputs(results, traces, out_dir, meta):
    os.makedirs(out_dir, exist_ok=True)
    # JSON
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump({"results": results, "traces": traces, "meta": meta}, f, ensure_ascii=False, indent=2)

    # CSV summary
    csv_path = os.path.join(out_dir, "summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["parameter","answer","confidence"])
        for r in results:
            w.writerow([r.get("parameter",""), r.get("answer",""), r.get("confidence","")])
