#!/usr/bin/env bash
# Regenerate every Creatte Tool icon: the brand SVGs (packaging/brand/generate.py), then the app
# icon in every size and format, the tray icons and the twelve app icons.
# Needs: python3 with fonttools and cairosvg (pip install fonttools cairosvg), cargo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/assets/app-icon"
BRAND="$ROOT/assets/brand"
ID="jp.creatte.creatte-tool"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 "$ROOT/packaging/brand/generate.py" "$ROOT"

render() { python3 -c 'import sys, cairosvg; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[3], output_width=int(sys.argv[2]), output_height=int(sys.argv[2]))' "$1" "$2" "$3"; }

SVG="$BRAND/creatte-mark.svg"
render "$SVG" 1024 "$DIR/creatte-tool-1024.png"
for s in 16 24 32 48 64 128 256 512; do
  mkdir -p "$DIR/hicolor/${s}x${s}/apps"
  render "$SVG" "$s" "$DIR/hicolor/${s}x${s}/apps/$ID.png"
done
mkdir -p "$DIR/hicolor/scalable/apps"
cp "$SVG" "$DIR/hicolor/scalable/apps/$ID.svg"
cp "$SVG" "$DIR/creatte-tool.svg"

ICO_PNGS=()
for s in 16 20 24 32 40 48 64 128 256; do render "$SVG" "$s" "$TMP/ico-$s.png"; ICO_PNGS+=("$TMP/ico-$s.png"); done
(cd "$ROOT" && cargo run -q -p xtask -- ico "$DIR/creatte-tool.ico" "${ICO_PNGS[@]}")

ICNS_PNGS=()
for s in 16 32 64 128 256 512 1024; do render "$SVG" "$s" "$TMP/icns-$s.png"; ICNS_PNGS+=("$TMP/icns-$s.png"); done
(cd "$ROOT" && cargo run -q -p xtask -- icns "$DIR/creatte-tool.icns" "${ICNS_PNGS[@]}")

# Tray: the black template mark for the macOS menu bar (44 px = 22 pt @2x), the colour mark elsewhere.
render "$BRAND/creatte-mark-black.svg" 44 "$BRAND/creatte-mark-black-44.png"
render "$SVG" 64 "$BRAND/creatte-mark-64.png"

for f in "$BRAND"/app-icons/*.svg; do render "$f" 128 "$ROOT/assets/app-icons/$(basename "${f%.svg}").png"; done
echo "icons written"
python3 -c 'import sys, cairosvg
for n in ("creatte-tool-wordmark", "creatte-tool-wordmark-white"):
    cairosvg.svg2png(url=f"{sys.argv[1]}/{n}.svg", write_to=f"{sys.argv[1]}/{n}.png", output_height=136)' "$BRAND"
