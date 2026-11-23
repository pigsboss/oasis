#!/usr/bin/env bash
# Fetch the Gaia DR3 XP continuous-mean-spectrum mirror.
#
# Manifest and files live under:
#   https://159.226.170.25/mirror/Gaia/dr3/Spectroscopy/xp_continuous_mean_spectrum/
#
# The mirror certificate does not match its IP address, so wget/aria2 must
# disable certificate verification for this host.  The manifest is fetched
# with wget, then aria2c downloads the 3386 shards in parallel.
#
# Usage:
#   tools/fetch-gdr3-xp.sh [--dest DIR] [--jobs 4] [--connections 8]
#                          [--split 8] [--limit N] [--dry-run]
#                          [--no-verify] [--allow-low-space]
#
# Expected raw size: ~3.61 TB (3386 shards).  Verify space before running.
set -euo pipefail

BASE_URL="${XP_BASE_URL:-https://159.226.170.25/mirror/Gaia/dr3/Spectroscopy/xp_continuous_mean_spectrum}"
DEST="${XP_DEST:-/mnt/data/huo/Datasets/Gaia/gdr3/xp_continuous_mean_spectrum}"
JOBS=4
CONNECTIONS=8
SPLITS=8
LIMIT=""
DRY_RUN=0
VERIFY=1
ALLOW_LOW_SPACE=0
EXPECTED_BYTES=$((3610 * 1000 * 1000 * 1000))  # ~3.61 TB
MIN_FREE_BYTES=$((3800 * 1000 * 1000 * 1000))

while (($#)); do
  case "$1" in
    --dest) DEST="${2:?--dest needs DIR}"; shift 2 ;;
    --jobs) JOBS="${2:?--jobs needs N}"; shift 2 ;;
    --connections) CONNECTIONS="${2:?--connections needs N}"; shift 2 ;;
    --split) SPLITS="${2:?--split needs N}"; shift 2 ;;
    --limit) LIMIT="${2:?--limit needs N}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-verify) VERIFY=0; shift ;;
    --allow-low-space) ALLOW_LOW_SPACE=1; shift ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$DEST"
MANIFEST="$DEST/_MD5SUM.txt"
URLS="$DEST/_aria2_urls.txt"

echo "== manifest =="
wget --no-check-certificate -q -O "$MANIFEST" "$BASE_URL/_MD5SUM.txt"
lines=$(wc -l < "$MANIFEST")
echo "manifest: $MANIFEST ($lines entries)"
if [[ "$lines" -lt 3000 ]]; then
  echo "error: manifest looks incomplete" >&2; exit 2
fi

# Validate every line: 32 hex chars, two spaces, a safe basename.
awk 'NF != 2 || $1 !~ /^[0-9a-fA-F]{32}$/ || $2 !~ /^[A-Za-z0-9._-]+$/ {bad=1; print "bad manifest line: " $0 > "/dev/stderr"} END {exit bad}' "$MANIFEST"
awk -v base="$BASE_URL" -v limit="$LIMIT" '
  limit != "" && NR > limit {exit}
  {printf "%s/%s\n", base, $2}
' "$MANIFEST" > "$URLS"
count=$(wc -l < "$URLS")
echo "urls: $URLS ($count files)"
echo "dest: $DEST"
echo "expected raw payload: ~3.61 TB"

free_bytes=$(df -PB1 "$DEST" | awk 'NR==2 {print $4}')
echo "free bytes: $free_bytes"
if (( free_bytes < MIN_FREE_BYTES && ! ALLOW_LOW_SPACE )); then
  echo "warning: free space is below 3.8 TB; use --allow-low-space only if you have another volume." >&2
  exit 3
fi

if (( DRY_RUN )); then
  echo "dry-run: manifest/url list written; nothing downloaded"
  echo "first URL: $(head -1 "$URLS")"
  exit 0
fi
command -v aria2c >/dev/null 2>&1 || {
  echo "error: aria2c not found; install aria2 first (e.g. emerge net-misc/aria2)" >&2
  exit 2
}

echo "== aria2c ($count files, -j $JOBS, -x $CONNECTIONS, -s $SPLITS) =="
aria2c \
  --input-file="$URLS" \
  --dir="$DEST" \
  --continue=true \
  --max-concurrent-downloads="$JOBS" \
  --max-connection-per-server="$CONNECTIONS" \
  --split="$SPLITS" \
  --min-split-size=1M \
  --file-allocation=none \
  --auto-file-renaming=false \
  --allow-overwrite=false \
  --check-certificate=false \
  --summary-interval=60 \
  --console-log-level=warn

if (( VERIFY )); then
  echo "== md5 verify =="
  ( cd "$DEST" && md5sum -c _MD5SUM.txt )
fi
echo "done: $DEST"
