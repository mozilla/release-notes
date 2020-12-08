#!/usr/bin/env python

import json
import os
import sys
from pathlib import Path
from shutil import rmtree

import requests

RELEASES_URL = os.getenv('RELEASES_URL', 'https://nucleus.mozilla.org/rna/all-releases.json')
OUTPUT_DIR = Path(__file__).with_name('releases')
LAST_MODIFIED = OUTPUT_DIR.joinpath('.last-modified')


def get_request_headers():
    headers = {}
    if LAST_MODIFIED.exists():
        with LAST_MODIFIED.open() as fh:
            headers['If-Modified-Since'] = fh.read()

    return headers


def get_release_data(everything):
    last_modified = None
    if everything:
        resp = requests.get(RELEASES_URL, {'all': 'true'}, timeout=60)
    else:
        headers = get_request_headers()
        resp = requests.get(RELEASES_URL, headers=headers, timeout=30)

    resp.raise_for_status()
    if resp.status_code == 304:
        # no updates, nothing modified since last_modified
        return None, None

    if 'last-modified' in resp.headers:
        last_modified = resp.headers['last-modified']

    return resp.json(), last_modified


def cleanup():
    rmtree(str(OUTPUT_DIR), ignore_errors=True)
    OUTPUT_DIR.mkdir()


def write_files(release_data, last_modified=None):
    for release in release_data:
        with OUTPUT_DIR.joinpath('%s.json' % release['slug']).open('w') as fp:
            json.dump(release, fp, indent=2, sort_keys=True)

    if last_modified:
        with LAST_MODIFIED.open('w') as fh:
            fh.write(last_modified)

    print('Wrote {} files'.format(len(release_data)))


def main(everything):
    try:
        data, last_modified = get_release_data(everything)
    except requests.RequestException as e:
        return 'ERROR: %s' % e
    if data:
        if everything:
            cleanup()

        write_files(data, last_modified)
    else:
        print('Releases are up to date. No update required.')


if __name__ == '__main__':
    sys.exit(main(sys.argv[-1] == '--all'))
