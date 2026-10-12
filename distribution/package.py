#!/usr/bin/env python3
"""Assembles the Creatte Film hand-out ZIP (UTF-8 file names, so Windows shows the Japanese
names correctly): installers in Mac/ and Windows/, the install guide, licences and checksums.

Usage: python3 distribution/package.py <artifacts dir> <version> <out.zip>
"""
import hashlib
import os
import shutil
import sys
import zipfile

art, version, out = sys.argv[1], sys.argv[2], sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
name = f"Creatte-Film-{version}"
stage = os.path.join(os.path.dirname(os.path.abspath(out)), "stage", name)
shutil.rmtree(os.path.dirname(stage), ignore_errors=True)
for sub in ("Mac", "Windows", "ライセンス"):
    os.makedirs(os.path.join(stage, sub))


def find(fname):
    for d, _, fs in os.walk(art):
        if fname in fs:
            return os.path.join(d, fname)
    sys.exit(f"missing {fname} in {art}")


files = {
    "Mac": [f"creatte-film-{version}-macos-universal.dmg"],
    "Windows": [f"creatte-film-{version}-windows-x64.msi", f"creatte-film-{version}-windows-arm64.msi"],
}
sums = []
for sub, names in files.items():
    for n in names:
        dst = os.path.join(stage, sub, n)
        shutil.copy(find(n), dst)
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        sums.append(f"{h}  {sub}/{n}")
open(os.path.join(stage, "SHA256SUMS.txt"), "w").write("\n".join(sums) + "\n")
for f in ("インストール手順.html", "インストール手順.pdf", "はじめにお読みください.txt"):
    shutil.copy(os.path.join(here, f), stage)
for f in ("LICENSE-MIT", "LICENSE-APACHE", "NOTICE"):
    shutil.copy(os.path.join(root, f), os.path.join(stage, "ライセンス"))
for d, _, fs in os.walk(os.path.join(root, "assets", "fonts")):
    for f in fs:
        if f.startswith("OFL-") and f.endswith(".txt"):
            shutil.copy(os.path.join(d, f), os.path.join(stage, "ライセンス"))
fonts = os.environ.get("CRAFT_FONTS_DIR")
if fonts:
    for fam in sorted(os.listdir(os.path.join(fonts, "fonts"))):
        lic = os.path.join(fonts, "fonts", fam, "OFL.txt")
        if os.path.isfile(lic):
            shutil.copy(lic, os.path.join(stage, "ライセンス", f"OFL-{fam}.txt"))
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    base = os.path.dirname(stage)
    for d, _, fs in os.walk(stage):
        for f in sorted(fs):
            full = os.path.join(d, f)
            z.write(full, os.path.relpath(full, base))
print(f"wrote {out}")
