import os, json, subprocess, sys, pathlib

def main():
    base = pathlib.Path(__file__).resolve().parents[1]
    pdf = base / "data" / "tender_sample.pdf"
    params = base / "config" / "parameters.json"
    out = base / "out_test"

    cmd = [sys.executable, str(base/"main.py"), "--pdf", str(pdf), "--params", str(params), "--out", str(out), "--mock"]
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        sys.exit(res.returncode)
    print("OK. See:", out)

if __name__ == "__main__":
    main()
