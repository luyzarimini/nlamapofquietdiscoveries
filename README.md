# The Netherlands — A Map of Quiet Discoveries

An illustrated journal spread of the Netherlands, drawn as a single hand-inked
SVG on warm watercolour paper — in the manner of a traveller's notebook.

> *There is no need to rush — discovery happens one quiet place at a time.*

## What it does

- **An imaginary map**, not a literal one: wandering dotted paths, a river of
  ink, tiny hand-drawn scenes (windmills, canal houses, a lighthouse, Spinoza's
  spectacles, Huygens' pendulum clock…) and a small open door near the centre
  that stands for curiosity.
- **Hover** (or touch) a drawing and a dotted ring appears around it.
- **Click** a drawing to open its own papyrus page, where every place is a
  **card** — with a short note, its address, and a Google Maps
  **route from Utrecht Centraal** (transit).
- **Tick** the places you've seen; **add your own** places as cards — each new
  card automatically gets its own route link.

Everything is one self-contained `index.html`: the two handwriting fonts
(Caveat, Reenie Beanie) are inlined as data URIs; there are no external
requests, no build dependencies at runtime.

## Files

| path | purpose |
| --- | --- |
| `index.html` | the finished page — open it in any browser |
| `src/template.html` | the source page, with `__CAVEAT__` / `__REENIE__` font placeholders |
| `src/fonts/*.woff2` | the two handwriting fonts (latin subsets, Google Fonts, OFL) |
| `src/build.py` | inlines the fonts and writes `index.html` |

## Rebuild

```
python src/build.py
```

## Notes

- Ticks and added cards live for the current session only (no storage yet).
- Fonts: [Caveat](https://fonts.google.com/specimen/Caveat) and
  [Reenie Beanie](https://fonts.google.com/specimen/Reenie+Beanie), both under
  the SIL Open Font License.
