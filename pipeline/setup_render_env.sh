#!/usr/bin/env bash
# One-time (aur sandbox restart ke baad) render environment setup.
# Remotion ka headless Chrome: libnss3 / libnspr4 chahiye, warna "Failed to launch the browser".
set -e
cd "$(dirname "$0")/.."
if ! ls /usr/lib/x86_64-linux-gnu/libnspr4.so >/dev/null 2>&1; then
  echo "[setup] installing Chrome system libs (libnss3, libnspr4)"
  sudo apt-get install -y -q libnss3 libnspr4 || sudo apt-get update -q && sudo apt-get install -y -q libnss3 libnspr4
fi
if [ ! -x remotion/node_modules/.bin/remotion ]; then
  echo "[setup] npm install (remotion)"
  (cd remotion && npm install --no-audit --no-fund)
fi
python3 -c "import PIL, edge_tts" 2>/dev/null || { echo "[setup] pip: pillow, edge-tts"; pip install -q pillow edge-tts; }
echo "[setup] OK"
