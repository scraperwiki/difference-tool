#!/bin/sh
dwdiff -i -c -A best text_from_url1 text_from_url2 | aha -w > /home/tool/http/diff.html
