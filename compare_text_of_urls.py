#!/usr/bin/env python

from __future__ import print_function
import json
import os
from os.path import join, dirname, abspath
import subprocess
import sys

from get_text_from_url import process_page


def main(argv=None):
    if argv is None:
        argv = sys.argv
    arg = argv[1:]

    # Enter two  URLs with a space between them
    if len(arg) > 0:
        # Developers can supply URL as an argument...
        urls = arg[0]
    else:
        # ... but normally the URL comes from the allSettings.json file
        with open(os.path.expanduser("~/allSettings.json")) as settings_json:
            settings = json.load(settings_json)
            url1 = settings['source-url']
            url2 = settings['source-url2']
    assert url1 and url2, 'Two URLs not entered.'
    diff_urls(url1, url2)


def diff_urls(url1, url2):
    text1 = process_page('text_from_url1', url1)
    text2 = process_page('text_from_url2', url2)
    subprocess.check_output("./diff_text.sh", cwd=dirname(abspath(__file__)))

if __name__ == '__main__':
    main()
