#!/usr/bin/env python

import json
import os
import sys
from pathlib import Path
from shutil import rmtree

import requests

RELEASES_URL = os.getenv('RELEASES_URL', 'https://nucleus.mozilla.org/rna/all-releases.json')
OUTPUT_DIR = Path(__file__).with_name('releases')
ETAG_FILE = OUTPUT_DIR.joinpath('.latest-update-etag')


def get_request_headers():
    headers = {}
    if ETAG_FILE.exists():
        with ETAG_FILE.open() as fh:
            headers['If-None-Match'] = fh.read()

    return headers


def get_release_data():
    etag = None
    headers = get_request_headers()
    resp = requests.get(RELEASES_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    if resp.status_code == 304:
        # no updates, etags match
        return None, None

    if 'etag' in resp.headers:
        etag = resp.headers['etag']

    return resp.json(), etag


def setup():
    rmtree(str(OUTPUT_DIR), ignore_errors=True)
    OUTPUT_DIR.mkdir()


def write_files(release_data, etag=None):
    for release in release_data:
        with OUTPUT_DIR.joinpath('%s.json' % release['slug']).open('w') as fp:
            json.dump(release, fp, indent=2, sort_keys=True)

    if etag:
        with ETAG_FILE.open('w') as fh:
            fh.write(etag)

    print('Wrote {} files'.format(len(release_data)))


def main():
    try:
        data, etag = get_release_data()
    except requests.RequestException as e:
        return 'ERROR: %s' % e
    if data:
        setup()
        write_files(data, etag)
    else:
        print('Releases are up to date. No update required.')


if __name__ == '__main__':
    sys.exit(main())
