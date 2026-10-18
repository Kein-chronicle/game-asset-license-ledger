import json, os, subprocess, sys, tempfile
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "license_ledger.py"); ok = True
d = tempfile.mkdtemp(); assets = os.path.join(d, "assets"); os.makedirs(assets)
for p in ["cc0-pack", "ccby-pack", "sa-pack", "nc-pack", "mixed-pack"]: os.makedirs(os.path.join(assets, p))
os.makedirs(os.path.join(assets, "_downloads"))                       # underscore dirs are not packs
ledger = {"packs": {"cc0-pack": {"license": "CC0-1.0", "source": "https://example.org/a"}, "ccby-pack": {"license": "CC-BY-4.0", "source": "https://example.org/b", "author": "Someone"},
          "sa-pack": {"license": "CC-BY-SA-4.0", "source": "https://example.org/c"}, "nc-pack": {"license": "CC-BY-NC-4.0", "source": "https://example.org/d"},
          "mixed-pack": {"license": "CC0-1.0", "source": "https://example.org/e", "mixed": True}, "ghost-pack": {"license": "MIT", "source": "x"}}}
lp = os.path.join(d, "l.json"); json.dump(ledger, open(lp, "w"))
def run(*x): p = subprocess.run([sys.executable, S, lp, "--assets", assets, *x], capture_output=True, text=True); return p.returncode, p.stdout
def expect(n, c, v=""):
    global ok; ok &= bool(c); print(("ok   " if c else "FAIL ") + n + ("" if c else f"\n     {v}"))
rc, out = run(); expect("non-commercial use: NC pack only warns, run passes", rc == 0 and "forbids commercial" in out, out)
rc, out = run("--commercial"); expect("commercial use: NC pack and mixed pack FAIL", rc == 1 and "nc-pack" in out and "mixed-pack" in out, out)
expect("share-alike is warned about", "sa-pack: CC-BY-SA-4.0 is share-alike" in out, out)
expect("ledger entry without a pack on disk is flagged stale", "ghost-pack: in the ledger but not on disk" in out, out)
os.makedirs(os.path.join(assets, "unlisted-pack"))
rc, out = run(); expect("a pack on disk with no ledger entry FAILS", rc == 1 and "unlisted-pack" in out, out)
os.rmdir(os.path.join(assets, "unlisted-pack"))
cp = os.path.join(d, "CREDITS.md"); run("--credits", cp); txt = open(cp).read()
expect("credits list every license that needs a notice (not CC0)", "ccby-pack" in txt and "cc0-pack" not in txt, txt)
e = os.path.join(d, "empty"); os.makedirs(e)
p = subprocess.run([sys.executable, S, lp, "--assets", e], capture_output=True, text=True); expect("empty assets dir is not a pass", p.returncode == 2, p.stdout)

# --- review findings
os.makedirs(os.path.join(assets, "_sneaky")); open(os.path.join(assets, "_sneaky", "x.png"), "w").write("x"); open(os.path.join(assets, "loose.png"), "w").write("x")
rc, out = run(); expect("files hiding in an underscore folder or loose in the root are WARNed, not skipped silently", rc == 0 and "_sneaky/: not scanned" in out and "loose.png" in out, out)
rc, out = run("--commercial"); expect("...and are FAILures in a commercial run", "FAIL _sneaky/" in out and "FAIL loose.png" in out, out)
led2 = json.load(open(lp)); led2["ignore"] = ["_sneaky", "loose.png"]; json.dump(led2, open(lp, "w"))
rc, out = run("--commercial"); expect("an explicit ignore list silences them", "_sneaky" not in out and "loose.png" not in out, out)
os.makedirs(os.path.join(assets, "mit-pack")); led2["packs"]["mit-pack"] = {"license": "MIT", "source": "https://example.org/m", "author": "A"}
led2["packs"]["nd-pack"] = {"license": "CC-BY-ND-4.0", "source": "https://example.org/nd"}; os.makedirs(os.path.join(assets, "nd-pack")); json.dump(led2, open(lp, "w"))
rc, out = run("--credits", cp); txt = open(cp).read(); expect("MIT and NC packs appear in the credits", "mit-pack" in txt and "nc-pack" in txt, txt)
rc, out = run("--commercial"); expect("ND is reported as 'forbids derivatives', not as a commercial ban", "nd-pack: CC-BY-ND-4.0 forbids derivatives" in out, out)
bad = os.path.join(d, "bad.json"); json.dump({"packs": []}, open(bad, "w"))
p = subprocess.run([sys.executable, S, bad, "--assets", assets], capture_output=True, text=True); expect("a ledger with the wrong shape is exit 2, not a traceback", p.returncode == 2 and "Traceback" not in p.stderr, p.stdout + p.stderr)
sys.exit(0 if ok else 1)
