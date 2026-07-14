# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-page interactive illustration: "The Netherlands — A Map of Quiet Discoveries," a hand-inked SVG journal map on watercolour paper. Clicking a drawing opens a papyrus-styled overlay ("sheet") where each place is a card with an address and a Google Maps route link from Utrecht Centraal. No framework, no dependencies, no external requests at runtime.

## Build

**Never edit `index.html` directly — it is generated.** Edit `src/template.html`, then:

```
python src/build.py
```

This inlines `src/fonts/*.woff2` as base64 into the `__CAVEAT__` / `__REENIE__` placeholders and wraps the body content in a standalone HTML skeleton (doctype, viewport, title).

`src/template.html` is body-content only (no doctype/head) because it doubles as a claude.ai Artifact, whose host adds the skeleton. Keep it that way; the standalone wrapper lives in `build.py`. The page was also published as a claude.ai artifact — republishing from another conversation requires passing that artifact's URL explicitly.

## Verifying changes

There are no tests; verification is visual, via headless Edge:

```
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu \
  --hide-scrollbars --window-size=1000,1500 --screenshot=out.png "file:///$(pwd -W)/index.html"
```

Gotchas learned the hard way:
- **Windows headless Chrome/Edge enforces a ~500px minimum window width.** To screenshot a real phone viewport, embed the page in a 390px-wide `<iframe>` harness page and screenshot that.
- To verify overlay content, append a snippet that calls `openSheet('<key>')` after the main `<script>` block of a throwaway copy.
- To verify clickability, use `document.elementFromPoint` at each `.spot`'s center (a real hit test) — script-invoked `openSheet` bypasses pointer handling and proves nothing about clicks. All icons must be on-screen for this (viewport-relative).

## Architecture

Everything lives in `src/template.html`: CSS, one large inline SVG (viewBox 1000×1440), the overlay sheet markup, and a script with the place data.

- **Clickable drawings** are `<g class="spot" data-key="...">` groups inside the SVG, each containing an invisible `rect.hit`, a dotted `circle.halo` (hover ring), the artwork, and a `text.label`. `data-key` indexes into the `DATA` object in the script.
- **Pointer-events invariant:** decorative full-page layers (paper grain, vignette, stains) are painted *after* the spots and would swallow clicks. The rule `.page > *{pointer-events:none}` + `.page > .spot{pointer-events:auto}` keeps only drawings interactive. Anything new added to the SVG must respect this.
- **`DATA`** maps each key to `{title, tag, places:[{n, s, loc, q}]}`. `loc` is the displayed address; `q` is the Google Maps destination query — omit both for imaginative/non-real entries (see `door`), which then render without address or route link. Route URLs are built in `routeHref()` (origin fixed to Utrecht Centraal, transit mode).
- **The sheet** (`.backdrop`/`.sheet`) renders places as cards via `makeCard()`; user-added cards get `card-user` styling and an auto-generated route query (`<input> + addPlace()`). Ticks and added cards are in-memory only — no persistence (known limitation; localStorage has been discussed but deliberately not added yet).
- **Hand-drawn look** comes from SVG turbulence/displacement filters (`#torn`, `#rough`, `#rough2`, `#tornSheet`) applied to shapes and borders; reuse them rather than drawing "wobbly" paths manually.

## Design constraints

- Muted palette only, defined as CSS custom properties on `:root` (`--paper`, `--ink`, `--ochre`, `--dust`, `--teal`, `--terra`, `--navy`, `--olive`, `--rust`). No saturated colors; derive everything from these tokens.
- Two fonts, both inlined: Caveat (titles/place names) and Reenie Beanie (marginalia/small notes). Do not add webfont links — a strict CSP blocks external hosts when served as an artifact.
- The page deliberately renders the same warm-paper world in light and dark themes (single-theme by choice).
- Touch devices have no hover: `@media (hover:none)` shows every halo faintly so drawings read as tappable. Keep hover-only affordances mirrored there.
