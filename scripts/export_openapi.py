#!/usr/bin/env python3
"""Export the locally generated YDL API contract as a safe static snapshot.

Requires only Python 3's standard library when Django returns JSON.
If the endpoint returns YAML, install PyYAML locally and rerun.
"""
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8000/?format=openapi')
    parser.add_argument('--output', default='api-docs/openapi.json')
    args = parser.parse_args()
    request = Request(args.url, headers={'Accept': 'application/json, application/openapi+json, application/yaml, */*'})
    with urlopen(request, timeout=30) as response:
        raw = response.read()
    try:
        spec = json.loads(raw.decode('utf-8-sig'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        try:
            import yaml
        except ImportError as error:
            raise SystemExit('The endpoint did not return JSON. If it returned YAML, run: python3 -m pip install PyYAML') from error
        spec = yaml.safe_load(raw.decode('utf-8-sig'))

    if not isinstance(spec, dict):
        raise SystemExit('Unexpected API specification: expected a JSON/YAML object')
    if 'swagger' in spec:
        if str(spec['swagger']) != '2.0':
            raise SystemExit('Expected Swagger 2.0; got ' + str(spec['swagger']))
        spec['host'] = 'api.example.invalid'
        spec['schemes'] = ['https']
    elif 'openapi' in spec:
        spec['servers'] = [{'url': 'https://api.example.invalid', 'description': 'Nonexistent placeholder — documentation only'}]
    else:
        raise SystemExit('Cannot find swagger or openapi version field. Verify the URL and response format.')

    if not isinstance(spec.get('paths'), dict) or not spec['paths']:
        raise SystemExit('No paths found in exported specification')
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Saved', dest, 'with', len(spec['paths']), 'path entries')
    print('API hostname replaced with api.example.invalid (reserved nonexistent domain).')
    print('REVIEW THE EXPORTED FILE BEFORE COMMITTING for private fields, contact data, examples or secrets.')


if __name__ == '__main__':
    main()
