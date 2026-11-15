#!/usr/bin/env bash
# Prepare the exact static site that GitHub Pages will publish.
# Run from any directory: bash scripts/prepare_api_docs.sh /tmp/ydl-api-preview
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/api-docs"
output_dir="${1:?Usage: bash scripts/prepare_api_docs.sh OUTPUT_DIRECTORY}"

if [[ -e "$output_dir" && ! -d "$output_dir" ]]; then
  echo "Output is not a directory: $output_dir" >&2
  exit 1
fi

for relative in \
  index.html \
  app.js \
  openapi.json \
  vendor/swagger-ui.css \
  vendor/swagger-ui-bundle.js \
  vendor/LICENSE \
  vendor/NOTICE; do
  if [[ ! -s "$source_dir/$relative" ]]; then
    echo "Missing or empty: api-docs/$relative" >&2
    exit 1
  fi
done

python3 -m json.tool "$source_dir/openapi.json" >/dev/null

mkdir -p "$output_dir/vendor"
cp "$source_dir/index.html" \
   "$source_dir/app.js" \
   "$source_dir/openapi.json" \
   "$output_dir/"
cp "$source_dir/vendor/swagger-ui.css" \
   "$source_dir/vendor/swagger-ui-bundle.js" \
   "$source_dir/vendor/LICENSE" \
   "$source_dir/vendor/NOTICE" \
   "$output_dir/vendor/"

printf 'Static API documentation prepared at: %s\n' "$output_dir"
