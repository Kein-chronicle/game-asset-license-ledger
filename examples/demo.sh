#!/usr/bin/env bash
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
echo "# Non-commercial project: the NC pack only warns"
run python3 scripts/license_ledger.py examples/ledger.json --assets examples/assets
echo "# Commercial release: the NC pack blocks"
run python3 scripts/license_ledger.py examples/ledger.json --assets examples/assets --commercial
echo "# A pack on disk with no ledger entry fails"
tmp=.demo-tmp; rm -rf "$tmp"; mkdir "$tmp"; cp -R examples/assets "$tmp/assets"; mkdir "$tmp/assets/mystery-pack"
run python3 scripts/license_ledger.py examples/ledger.json --assets "$tmp/assets"
rm -rf "$tmp"
