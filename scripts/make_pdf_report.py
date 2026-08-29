#!/usr/bin/env python3
"""
Dependency-free minimal PDF writer for Movie Enigma audit reports.
Usage: python make_pdf_report.py [input.txt] [-o report.pdf]
If no input file is given, the built-in audit summary is used.
"""
import sys

BUILTIN = """BITCOIN MOVIE ENIGMA - AUDIT SUMMARY (2026-08-29)
Escrow: bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6 (100,000 sats)

FINDING 1: starter package math claim wrong.
Claimed ~8.2M checksum-valid candidates; real ~512K (24-word checksum = 8 bits).

FINDING 2 (FATAL): current 34-word list cannot contain the solution.
'goon' and 'shark' are not BIP39 words; all combos with them are rejected.

Word list (errors marked): hard glory alien mad motion now escape goon[X]
sun possible ill life good eye river warrior clock hope gravity first
solar blade planet ordinary bar shark[X] boy cream matrix story ghost
soft shine human

HYPOTHESIS H-BME1: transformation rule = BIP39 word literally in title
(example: Sharknado -> tornado). Panel 8 (Goonies) needs re-identification.

Conflicting panels: 3, 5, 9, 13, 14, 16, 23, 24, 27.
"""

def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

def build_pdf(lines, path):
    per_page = 54
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)] or [[""]]
    objs = []
    npages = len(pages)
    kids = " ".join(f"{3 + i * 2} 0 R" for i in range(npages))
    objs.append(f"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n")
    objs.append(f"2 0 obj<</Type/Pages/Kids[{kids}]/Count {npages}>>endobj\n")
    font_id = 3 + npages * 2
    for i, pg in enumerate(pages):
        content = "BT /F1 9 Tf 40 760 12 TL\n"
        for ln in pg:
            content += f"({esc(ln)}) Tj T*\n"
        content += "ET"
        objs.append(f"{3 + i * 2} 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]"
                    f"/Resources<</Font<</F1 {font_id} 0 R>>>>/Contents {4 + i * 2} 0 R>>endobj\n")
        objs.append(f"{4 + i * 2} 0 obj<</Length {len(content)}>>stream\n{content}endstream endobj\n")
    objs.append(f"{font_id} 0 obj<</Type/Font/Subtype/Type1/BaseFont/Courier>>endobj\n")

    out = "%PDF-1.4\n"
    offsets = []
    for o in objs:
        offsets.append(len(out.encode()))
        out += o
    xref_pos = len(out.encode())
    n = len(objs) + 1
    out += f"xref\n0 {n}\n0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n"
    out += f"trailer<</Size {n}/Root 1 0 R>>\nstartxref\n{xref_pos}\n%%EOF\n"
    with open(path, "wb") as fh:
        fh.write(out.encode("latin-1"))
    print(f"[DONE] wrote {path} ({npages} page(s))")

def main():
    args = sys.argv[1:]
    out, inp, i = "movie_enigma_report.pdf", None, 0
    while i < len(args):
        if args[i] == "-o":
            out = args[i + 1]; i += 2
        else:
            inp = args[i]; i += 1
    text = open(inp, encoding="utf-8").read() if inp else BUILTIN
    build_pdf(text.splitlines(), out)

if __name__ == "__main__":
    main()
