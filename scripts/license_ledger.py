#!/usr/bin/env python3
"""asset-license-ledger: every asset pack on disk must have a ledger entry; commercial-use risk is classified; credits are generated.
usage: license_ledger.py ledger.json --assets DIR [--commercial] [--credits CREDITS.md]
ledger.json: {"packs": {"<dir name>": {"license": "CC0-1.0", "source": "https://...", "author": "...", "mixed": false}}, "ignore": ["_downloads"]}
Folders starting with "." or "_" and loose files are not packs, but they are never skipped silently: each one that holds files is reported (WARN, or FAIL with --commercial
unless it is named in "ignore"). Credits list every license that needs a notice (everything except CC0/Unlicense/0BSD), including MIT, ISC and the NC licenses.
exit 0 ok | 1 problems | 2 bad input"""
import argparse, json, os, sys
OK_NO_ATTR = {"CC0-1.0", "Unlicense", "0BSD"}
ATTR = {"CC-BY-4.0", "CC-BY-3.0", "OGA-BY-3.0", "OFL-1.1", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "MIT", "ISC"}      # allow commercial use but require a notice
SHARE_ALIKE = {"CC-BY-SA-4.0", "CC-BY-SA-3.0", "GPL-3.0", "GPL-2.0", "LGPL-3.0", "AGPL-3.0"}
NON_COMMERCIAL = {"CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "CC-BY-NC-3.0"}
NO_DERIVATIVES = {"CC-BY-ND-4.0", "CC-BY-ND-3.0"}      # commercial use is allowed, but editing, cropping or repacking the asset is a derivative

ap = argparse.ArgumentParser(); ap.add_argument("ledger"); ap.add_argument("--assets", required=True)
ap.add_argument("--commercial", action="store_true"); ap.add_argument("--credits")
a = ap.parse_args()
try:
    led = json.load(open(a.ledger, encoding="utf-8")); packs = led["packs"]; ignore = set(led.get("ignore", []))
    assert isinstance(packs, dict) and all(isinstance(e, dict) and isinstance(e.get("license", ""), str) for e in packs.values())
except Exception as e: print(f"bad ledger: expected {{\"packs\": {{name: {{license, source}}}}}} ({type(e).__name__})"); sys.exit(2)
if not os.path.isdir(a.assets): print("bad assets dir"); sys.exit(2)
dirs = sorted(d for d in os.listdir(a.assets) if os.path.isdir(os.path.join(a.assets, d)) and not d.startswith((".", "_")))
if not dirs: print("assets dir has no packs: an empty scan proves nothing"); sys.exit(2)
errs, warns = [], []
def has_files(p): return any(fs for _, _, fs in os.walk(p) if any(f not in (".DS_Store", "Thumbs.db", ".keep") for f in fs))
for name in sorted(os.listdir(a.assets)):
    full = os.path.join(a.assets, name)
    if name in (".DS_Store", "Thumbs.db") or name in dirs or name in ignore: continue
    if os.path.isdir(full):
        if has_files(full): (errs if a.commercial else warns).append(f"{name}/: not scanned as a pack (name starts with '.' or '_') but it holds files - license unknown. Add it to the ledger 'ignore' list if it is not part of the product")
    else: (errs if a.commercial else warns).append(f"{name}: loose file in the assets folder, not in any pack - license unknown")
for d in dirs:
    e = packs.get(d)
    if not e: errs.append(f"{d}: on disk but NOT in the ledger (unknown license = unusable)"); continue
    lic = e.get("license", "").strip()
    if not lic: errs.append(f"{d}: empty license"); continue
    if not e.get("source"): warns.append(f"{d}: no source URL (you cannot re-verify the license later)")
    if e.get("mixed"): errs.append(f"{d}: license is MIXED per file - check the pack's own credits file per asset before use") if a.commercial else warns.append(f"{d}: mixed licenses - check per file")
    if lic in NON_COMMERCIAL: (errs if a.commercial else warns).append(f"{d}: {lic} forbids commercial use / derivatives")
    elif lic in NO_DERIVATIVES: (errs if a.commercial else warns).append(f"{d}: {lic} forbids derivatives: cropping, recolouring or packing into an atlas counts, so it is usable only unmodified")
    elif lic in SHARE_ALIKE: warns.append(f"{d}: {lic} is share-alike/copyleft - derivatives must carry the same license; think before bundling in a closed product")
    elif lic not in OK_NO_ATTR | ATTR | SHARE_ALIKE | NON_COMMERCIAL | NO_DERIVATIVES: errs.append(f"{d}: unrecognised license id '{lic}' (use SPDX ids)")
for d in packs:
    if d not in dirs: warns.append(f"{d}: in the ledger but not on disk (stale entry)")
if a.credits:
    rows = [f"- **{d}** - {packs[d].get('author', 'unknown author')} - {packs[d]['license']} - {packs[d].get('source', '')}" for d in dirs if d in packs and packs[d].get("license") not in OK_NO_ATTR and packs[d].get("license")]
    open(a.credits, "w", encoding="utf-8").write("# Credits\n\nAttribution required by the licenses below.\n\n" + "\n".join(rows) + "\n")
for w in warns: print("WARN", w)
for e in errs: print("FAIL", e)
print(f"{len(dirs)} packs scanned; " + ("problems found" if errs else "ledger complete"))
sys.exit(1 if errs else 0)
