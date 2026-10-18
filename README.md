# game-asset-license-ledger

**Keep a license ledger for downloaded art and audio packs: fail on unknown packs, non-commercial licenses in a commercial release, and generate credits.**

[![test](https://github.com/Kein-chronicle/game-asset-license-ledger/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/game-asset-license-ledger/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

Asset packs arrive one at a time and their licenses are forgotten. The ledger maps each pack folder to a license and source; the check compares it with what is actually on disk.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/game-asset-license-ledger.git ~/.claude/skills/asset-license-ledger
```

For a single project, clone into `<project>/.claude/skills/asset-license-ledger` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/game-asset-license-ledger.git
cd game-asset-license-ledger
```

**Requires:** Python 3.10+.

## Quick start

Check three packs:

```console
$ bash examples/demo.sh
# Non-commercial project: the NC pack only warns
$ python3 scripts/license_ledger.py examples/ledger.json --assets examples/assets
WARN nc-music: CC-BY-NC-4.0 forbids commercial use / derivatives
WARN cc0-ui: in the ledger but not on disk (stale entry)
FAIL kenney-ui: on disk but NOT in the ledger (unknown license = unusable)
3 packs scanned; problems found
[exit 1]

# Commercial release: the NC pack blocks
$ python3 scripts/license_ledger.py examples/ledger.json --assets examples/assets --commercial
WARN cc0-ui: in the ledger but not on disk (stale entry)
FAIL kenney-ui: on disk but NOT in the ledger (unknown license = unusable)
FAIL nc-music: CC-BY-NC-4.0 forbids commercial use / derivatives
3 packs scanned; problems found
[exit 1]

# A pack on disk with no ledger entry fails
$ python3 scripts/license_ledger.py examples/ledger.json --assets .demo-tmp/assets
WARN nc-music: CC-BY-NC-4.0 forbids commercial use / derivatives
WARN cc0-ui: in the ledger but not on disk (stale entry)
FAIL kenney-ui: on disk but NOT in the ledger (unknown license = unusable)
FAIL mystery-pack: on disk but NOT in the ledger (unknown license = unusable)
4 packs scanned; problems found
[exit 1]
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/license_ledger.py ledger.json --assets ./assets --commercial --credits CREDITS.md
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- A pack on disk with no ledger entry fails (unknown license means unusable); a ledger entry with no pack on disk is flagged stale.
- With `--commercial`, non-commercial, no-derivatives and mixed packs fail; share-alike licenses are warned about. Folders starting with `.` or `_` and loose files are reported (and fail a commercial run) unless the ledger's `ignore` list names them.
- `--credits FILE` writes attributions for the licenses that require them (not CC0).
- An empty assets directory is exit `2`, not a pass.

## Limits

- It trusts the license you wrote in the ledger; it does not inspect the pack.
- Not legal advice.

## Related projects

These solve neighbouring problems; use them when they fit better.

- **REUSE (FSFE)**: license metadata for source files
- **license-checker (npm)**: licenses of code dependencies, not art packs

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**canvas-render-pixel-gate**](https://github.com/Kein-chronicle/canvas-render-pixel-gate): Detect grey-box screenshots: measure unique colors and flat-fill share of a rendered game canvas, and refuse to pass what it could not measure.
- [**web-game-asset-reality-check**](https://github.com/Kein-chronicle/web-game-asset-reality-check): Catch web-game bugs the type checker can't: fonts that are declared but not shipped, runtime CDN dependencies, and page errors from headless Chromium.
- [**ffmpeg-video-qa-gates**](https://github.com/Kein-chronicle/ffmpeg-video-qa-gates): Machine QA for short videos with ffmpeg: frozen frames, dead air, loudness, true peak, size, a busy opening, and readable subtitle timing.

## Development

```sh
python3 tests/run.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: licenses, assets, game-development, compliance, creative-commons, credits, claude-skills</sub>
