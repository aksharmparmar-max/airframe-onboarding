# Airframe CAD Onboarding — site

The onboarding project for new ASME Aero Airframe subteam members: design a motor
mount in Fusion 360. Published as a single static page.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole site. One self-contained file — images are inlined, no CSS/JS dependencies. |
| `files/` | The three reference CAD files members download, plus a zip of all three. |
| `robots.txt` | Keeps the site out of search results. The page also carries a `noindex` meta tag. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is rather than running them through Jekyll. |

## Editing the content

`index.html` is generated, so don't edit it directly — edits get overwritten on the
next build. The source is `template.html` plus `build.py` (kept with the working
files, not in this repo). The build inlines the images and swaps in download links.

For a small copy fix, editing `index.html` directly is fine as long as you make the
same change in the template.

## Deploying to GitHub Pages

The repo is already initialized and committed. To publish:

1. Create a new **public** repo on github.com — don't add a README, license, or
   .gitignore, since this folder already has commits.
2. Connect and push:

   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```

3. In the repo: **Settings → Pages → Source: Deploy from a branch**, branch `main`,
   folder `/ (root)`. Save.
4. Wait a minute or two. The site appears at
   `https://<your-username>.github.io/<repo-name>/`.

To update later: edit, then `git add -A && git commit -m "..." && git push`. Pages
redeploys on its own.

## Notes

- The page names team members and describes internal workflow, so it's set to
  `noindex` — anyone with the link can read it, but it won't surface in a search
  for someone's name. GitHub Pages can't password-protect on the free tier; if you
  need real access control later, Cloudflare Pages does it.
- The CAD files in `files/` are Fusion 360 native (`.f3d` / `.f3z`). Members on other
  CAD tools need STEP exports — worth adding to `files/` when you have them.
