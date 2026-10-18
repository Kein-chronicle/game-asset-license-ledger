---
name: asset-license-ledger
description: Keep a license ledger for downloaded game/art/audio/font asset packs so nothing with unknown, non-commercial or copyleft terms slips into a product. Use when you hoard free assets (CC0 packs, CC-BY, OGA, mixed repositories), when preparing a release, or when credits/attribution files must be generated. Checks every pack on disk has a ledger entry, classifies commercial-use risk, warns on share-alike and mixed-license repos, and writes CREDITS.md.
---

# asset-license-ledger

Rules for keeping free art, audio and font packs usable in a product:

- Keep the **original zips** next to the extracted copies (re-extractable) and record **source URL + license id + author** per pack.
- A repo's license is not its assets' license. A tool's code can be GPL while the sprites it ships are a per-contributor
  mix of CC0 / CC-BY / CC-BY-SA / OGA-BY. Mark such packs `mixed` and check the pack's own credits file per asset before using it.
- **CC-BY-SA / GPL are share-alike**: derivatives carry the same license. Fine for open work, a trap for a closed commercial game. NC / ND = no.
- Link, don't redistribute, when you publish a repo: ship the ledger and credits, not other people's files.
- Generated credits list every license that needs a notice or attribution (MIT, ISC, CC-BY, NC and so on); only CC0, Unlicense and 0BSD are left out.
- Folders starting with `.` or `_` and loose files are not scanned as packs, but they are reported when they hold files (and fail a `--commercial` run) unless the ledger's `"ignore"` list names them.
- ND licenses forbid derivatives (cropping, recolouring, packing into an atlas), which is a different restriction from NC.
- An unknown license is an unusable asset. A pack on disk with no ledger line fails the check.
- Not legal advice: the license-id lists in the script are a starting set.

```bash
python3 scripts/license_ledger.py ledger.json --assets assets/ --commercial --credits CREDITS.md
python3 tests/run.py
```
