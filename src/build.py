"""Generate the onboarding page from template.html.

    python src/build.py            -> index.html (the published site)
    python src/build.py artifact   -> src/artifact-build.html (untracked)

The page is emitted as ONE self-contained HTML file: images are inlined as
base64 data URIs and there is no external CSS or JS. That's deliberate — it
means the site has no build pipeline to break and no assets that can 404.

Two flavors exist because the page is published in two places:

  site      the GitHub Pages site, where the CAD files sit next to index.html
            and the file cards get real download links.
  artifact  a copy hosted on claude.ai, which can't host the CAD binaries, so
            the download links are replaced with a pointer to the shared folder.

Requires nothing but Python 3. Run it from anywhere; paths are resolved
relative to this file.
"""
import base64
import os
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SRC)

IMAGES = [("{{IMG1}}", "image1.jpg"), ("{{IMG2}}", "image2.jpg"), ("{{IMG3}}", "image3.jpg")]

DOWNLOADS = {
    "{{DL_MOTOR}}": "files/brushless-motor.f3d",
    "{{DL_ASSEMBLY}}": "files/brushless-motor-mount-assembly.f3z",
    "{{DL_MOUNT}}": "files/motor-mount.f3d",
}

ZIP = "files/airframe-cad-files.zip"

# A file served by a plain web host gets no document shell, and without a
# viewport tag phones render the page at desktop width.
FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%E2%9C%88%EF%B8%8F%3C/text%3E%3C/svg%3E"
)
HEAD_EXTRA = """<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<meta name="description" content="ASME Aero Airframe subteam onboarding: design a real motor mount in Fusion 360. Instructions, reference CAD files, and checkpoints." />
<link rel="icon" href="%s" />
""" % FAVICON


def kb(rel):
    return "%d KB" % round(os.path.getsize(os.path.join(SITE, rel)) / 1024)


def wrap_document(html):
    """Split the template at </style> and rebuild it as a complete document."""
    cut = html.index("</style>") + len("</style>")
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        + HEAD_EXTRA
        + html[:cut]
        + "\n</head>\n<body>\n"
        + html[cut:]
        + "\n</body>\n</html>\n"
    )


def render(mode):
    html = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()

    for token, name in IMAGES:
        with open(os.path.join(SRC, "img", name), "rb") as fh:
            html = html.replace(token, "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode())

    if mode == "site":
        html = html.replace("{{FILES_LINK_LABEL}}", "")
        for token, rel in DOWNLOADS.items():
            html = html.replace(
                token,
                '<a class="dl" href="%s" download>Download <span class="sz">%s</span></a>' % (rel, kb(rel)),
            )
        html = html.replace(
            "{{DL_ALL}}",
            '<a class="dl-all" href="%s" download>Download all three files '
            '<span class="sz">%s</span></a>' % (ZIP, kb(ZIP)),
        )
        html = wrap_document(html)
        out = os.path.join(SITE, "index.html")
    else:
        html = html.replace(
            "{{FILES_LINK_LABEL}}",
            " <em>&nbsp;·&nbsp; in the onboarding folder on the exec SharePoint</em>",
        )
        for token in DOWNLOADS:
            html = html.replace(token, "")
        html = html.replace("{{DL_ALL}}", "")
        out = os.path.join(SRC, "artifact-build.html")

    assert "{{" not in html, "unreplaced placeholder in %s build" % mode
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("%-8s -> %s (%d KB)" % (mode, out, round(os.path.getsize(out) / 1024)))


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "site")
