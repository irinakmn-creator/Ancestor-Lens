import re

MERGES = [
    {
        "canonical": "blog-what-nationality-look-like.html",
        "deprecated": "blog-what-nationality-i-look-like.html",
        "canonical_url": "https://ancestorlens.app/blog-what-nationality-look-like.html",
    },
    {
        "canonical": "blog-ai-vs-dna.html",
        "deprecated": "blog-dna-vs-ai.html",
        "canonical_url": "https://ancestorlens.app/blog-ai-vs-dna.html",
    },
    {
        "canonical": "blog-heritage-no-dna.html",
        "deprecated": "blog-ancestry-without-dna.html",
        "canonical_url": "https://ancestorlens.app/blog-heritage-no-dna.html",
    },
    {
        "canonical": "blog-roots-psychology.html",
        "deprecated": "blog-curiosity.html",
        "canonical_url": "https://ancestorlens.app/blog-roots-psychology.html",
    },
]

DEPRECATED_FILES = [m["deprecated"] for m in MERGES]
DEPRECATED_TO_CANONICAL = {m["deprecated"]: m["canonical"] for m in MERGES}

# 1. Overwrite deprecated files with redirect
REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={canonical_url}">
    <link rel="canonical" href="{canonical_url}">
    <title>Redirecting...</title>
    <script>window.location.href = "{canonical_url}";</script>
</head>
<body>
    <p>This page has moved. <a href="{canonical_url}">Click here</a>.</p>
</body>
</html>
"""

for merge in MERGES:
    with open(merge["deprecated"], "w") as f:
        f.write(REDIRECT_TEMPLATE.format(canonical_url=merge["canonical_url"]))
    print(f"Redirected: {merge['deprecated']} → {merge['canonical']}")

# 2. Update all internal links in all HTML files
import glob

html_files = glob.glob("*.html")
for filepath in html_files:
    if filepath in DEPRECATED_FILES:
        continue
    with open(filepath, "r") as f:
        content = f.read()
    modified = False
    for dep, can in DEPRECATED_TO_CANONICAL.items():
        if dep in content:
            content = content.replace(dep, can)
            print(f"  Fixed link in {filepath}: {dep} → {can}")
            modified = True
    if modified:
        with open(filepath, "w") as f:
            f.write(content)

print("\nDone.")
