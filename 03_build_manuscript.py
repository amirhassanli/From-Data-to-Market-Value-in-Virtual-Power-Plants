#!/usr/bin/env python3
"""
03_build_manuscript.py
1) fills every {{TOKEN}} in the manuscript from prisma_values.json / dmdi_values.json
2) renumbers citations [n] in order of first appearance (IEEE style) and re-sorts the reference list
3) writes supplementary_S1_final.csv with the final reference numbers
4) (optional) converts to .docx with pandoc

  python 03_build_manuscript.py --src manuscript.md --values prisma_values.json dmdi_values.json --out manuscript_filled.md
  python 03_build_manuscript.py --src manuscript.md --no-fill --out manuscript_renumbered.md     # numbering only
  add --docx to also call:  pandoc manuscript_filled.md -o manuscript_filled.docx
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def fill(text, value_files, allow_missing):
    vals = {}
    for f in value_files:
        vals.update(json.loads(Path(f).read_text(encoding="utf-8")))
    missing = sorted({m for m in TOKEN.findall(text) if m not in vals or str(vals[m]) in ("NA", "PENDING")})
    if missing and not allow_missing:
        print("UNFILLED / PENDING TOKENS:", ", ".join(missing))
        print("Run scripts 01 and 02 completely (or complete the screening / double coding) and retry.")
        sys.exit(1)
    return TOKEN.sub(lambda m: str(vals.get(m.group(1), m.group(0))), text)


def renumber(text):
    head, sep, refs = text.partition("\n# References\n")
    if not sep:
        sys.exit("Heading '# References' not found")
    entries = {}
    for line in refs.strip().splitlines():
        m = re.match(r"\[(\d+)\]\s+(.*)", line.strip())
        if m:
            entries[int(m.group(1))] = m.group(2)
    order = []
    for m in re.finditer(r"\[(\d+)\]", head):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    missing = [n for n in order if n not in entries]
    if missing:
        sys.exit(f"Cited but absent from reference list: {missing}")
    unused = sorted(set(entries) - set(order))
    if unused:
        print(f"WARNING: dropped uncited references (old numbers): {unused}")
    mp = {old: new for new, old in enumerate(order, 1)}
    head = re.sub(r"\[(\d+)\]", lambda m: f"[{mp[int(m.group(1))]}]", head)
    new_refs = "\n\n".join(f"[{mp[o]}] {entries[o]}" for o in order)
    return head + "\n# References\n\n" + new_refs + "\n", mp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--values", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-fill", action="store_true")
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--docx", action="store_true")
    a = ap.parse_args()
    text = Path(a.src).read_text(encoding="utf-8")
    if not a.no_fill:
        text = fill(text, a.values, a.allow_missing)
    text, mp = renumber(text)
    Path(a.out).write_text(text, encoding="utf-8")
    Path("ref_map.json").write_text(json.dumps(mp, indent=2))
    s1 = Path("supplementary_S1.csv")
    if s1.exists():
        import pandas as pd
        d = pd.read_csv(s1, dtype=str)
        d["ref_final"] = d["ref"].map(lambda x: mp.get(int(x), ""))
        d.to_csv("supplementary_S1_final.csv", index=False, encoding="utf-8-sig")
    print(f"Written {a.out}; {len(mp)} references numbered by first appearance.")
    if a.docx:
        subprocess.run(["pandoc", a.out, "-o", str(Path(a.out).with_suffix(".docx"))], check=True)


if __name__ == "__main__":
    main()
