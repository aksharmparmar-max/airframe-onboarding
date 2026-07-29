# Airframe CAD Onboarding — site

The onboarding project for new ASME Aero Airframe subteam members: design a motor
mount in Fusion 360.

**Live at <https://aksharmparmar-max.github.io/airframe-onboarding/>**

## What's here

| Path | What it is |
|---|---|
| `index.html` | The published page. **Generated — don't edit by hand.** |
| `src/` | What the page is built from: `template.html`, `build.py`, and `img/`. |
| `files/` | The three reference CAD files members download, plus a zip of all three. |
| `robots.txt` | Keeps the site out of search results. The page also carries a `noindex` meta tag. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is rather than running them through Jekyll. |

`index.html` is one self-contained file — images are inlined as data URIs and
there's no external CSS or JS. Nothing to install, nothing that can 404.

## Changing the content

Edit `src/template.html`, then regenerate:

```bash
python src/build.py
```

That rewrites `index.html`. Commit both the template change and the regenerated
`index.html` together, then push — GitHub Pages redeploys on its own within a
minute or two.

```bash
git add -A
git commit -m "Describe the change"
git push
```

To preview before pushing, open `index.html` in a browser, or serve the folder
with `python -m http.server 8765` and visit <http://localhost:8765> — the
download links only work when served, not opened as a file.

### The two build flavors

`python src/build.py` builds the site. `python src/build.py artifact` builds a
copy for hosting on claude.ai, which can't host the CAD binaries, so its download
links are replaced with a pointer to the shared folder. That output is
`src/artifact-build.html` and is intentionally untracked.

## How the page behaves

- **Track selector.** Readers pick Track A or Track B in "Pick a track" and the
  modules hide the other track's steps. The choice persists per browser.
- **Progress checkboxes.** Each step can be ticked off; progress saves to the
  reader's own browser only, and nothing is reported back to anyone. The total
  counts only the steps currently visible, so it adapts to the chosen track.
- Track columns are marked with `data-track="a"` / `data-track="b"` in the
  template. Any new step block needs one of those to be filtered correctly.

## Notes

- The page names team members and describes internal workflow, so it's set to
  `noindex`. Anyone with the link can read it, but it won't surface in a search
  for someone's name. GitHub Pages can't password-protect on the free tier; if
  you need real access control, Cloudflare Pages does it.
- The CAD files are Fusion 360 native (`.f3d` / `.f3z`). Members on other CAD
  tools need STEP exports — worth adding to `files/` when you have them, and
  updating the "File formats" callout in the template once you do.
