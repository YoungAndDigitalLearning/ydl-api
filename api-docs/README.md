# Y&D Learning API — Archived OpenAPI Documentation

This directory holds a **static, read-only Swagger UI** for the historical Django REST Framework backend of Young & Digital Learning (TU Berlin / SKB academic project).

**Live documentation:** https://younganddigitallearning.github.io/ydl-api/ (after enabling Pages and completing the workflow)

The specification is an exported snapshot of the _local_ backend, not an independently maintained or invented API contract. GitHub Pages does not run Django, and this documentation does not provide an API server.

## Update the API specification

With the YDL backend running on `127.0.0.1:8000`, from the root of the `ydl-api` submodule:

```bash
python3 scripts/export_openapi.py \
  --url 'http://127.0.0.1:8000/?format=openapi' \
  --output api-docs/openapi.json
```

The script accepts Swagger/OpenAPI 2.0 and OpenAPI 3.x **JSON**. If your endpoint produces YAML, install PyYAML in your local environment and rerun; the output is still JSON. The exported server hostname is replaced with `api.example.invalid`, a deliberately nonexistent placeholder.

**Before committing:** inspect `api-docs/openapi.json`. Verify that it contains no private URLs, personal contact details, proprietary examples, secrets or sensitive model metadata. The script only automatically replaces the top-level API hostname, **not** arbitrary embedded strings. The schema may include historically broad permissions or write endpoints; it is reference material, not a secure API.

```bash
python3 -m json.tool api-docs/openapi.json >/dev/null
```

## Publish on GitHub Pages

1. Commit the files in this directory, `scripts/export_openapi.py`, and `.github/workflows/deploy-api-docs.yml` to `feature/local-demo` in `ydl-api`.
2. Open `ydl-api` on GitHub → **Settings → Pages** → choose **GitHub Actions** as the source.
3. Run **Actions → Deploy archived API documentation → Run workflow** (or push to `feature/local-demo`).
4. Open `https://younganddigitallearning.github.io/ydl-api/`.

There is no need for a `gh-pages` branch: GitHub Actions uploads an isolated Pages artifact containing only the static UI, vendored CSS/JS, and the exported schema. The backend source is not published as website assets. The workflow pins `swagger-ui-dist` and installs it with pnpm 12.18.0 on Node.js 24.

## Local test

From the `ydl-api` submodule:

```bash
pnpm install --dir api-docs
mkdir -p api-docs/vendor
cp api-docs/node_modules/swagger-ui-dist/swagger-ui.css api-docs/vendor/
cp api-docs/node_modules/swagger-ui-dist/swagger-ui-bundle.js api-docs/vendor/
python3 -m http.server 4174 --directory api-docs
```

Open `http://127.0.0.1:4174/`. The generated `api-docs/vendor/` and `api-docs/node_modules/` directories should not be committed.

## Safety and limitations

- **Read-only:** Swagger UI uses `supportedSubmitMethods: []` and an interceptor that rejects all requests except loading the same-origin `openapi.json`.
- **No production server:** The placeholder server `https://api.example.invalid` intentionally does not resolve.
- **Static snapshot:** Update and recommit the JSON after API changes; it is not regenerated on GitHub Actions because the runner has no Django backend.
- **No credentials:** Do not enter tokens or passwords into the published docs.
- **Browser assets:** CSS/JS are copied from the pinned Swagger UI npm package into the site; the published UI does not depend on a CDN.

## Links

- [Backend source](https://github.com/YoungAndDigitalLearning/ydl-api)
- [Full-stack project](https://github.com/YoungAndDigitalLearning/ydl)
- [Interactive frontend demo](https://younganddigitallearning.github.io/)
