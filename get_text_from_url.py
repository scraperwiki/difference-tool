#!/usr/bin/env python
# encoding: utf-8

from __future__ import (unicode_literals, print_function,
                        absolute_import, division)
import codecs
import re
import requests
import sys

from os.path import join, dirname, abspath

import lxml.html
import lxml.html.clean


def read_file(input_filename):
    """ Return content of file. """
    with codecs.open(input_filename, 'r', encoding='utf-8') as f:
        return f.read()


def clean_html(content):
    """
    Take HTML content and return a cleaned root element.
    
    Removes styles, scripts, comments, links etc. from element
    and its child elements.

    See http://lxml.de/3.4/api/lxml.html.clean.Cleaner-class.html
    """
    # Remove line breaks in HTML; lxml includes these in text_content() otherwise.
    content = re.sub(r'(\r\n|\n|\r)+', ' ', content)
    root = lxml.html.fromstring(content)
    cleaner = lxml.html.clean.Cleaner(style=True)
    cleaned_html = cleaner.clean_html(root)
    for el in cleaned_html.xpath("//p|//br|//div"):
        el.tail = "\n\n" + el.tail if el.tail else "\n\n"
    return cleaned_html


def write_output(output_filename, element):
    """ Write text from HTML element and all child elements to output file. """
    output_path = join(dirname(abspath(__file__)), output_filename)
    text_content = element.text_content()
    #output_lines = [re.sub(u'^[\s\xa0]+|[ \t\xa0]+$', '', line + '\n')
    #                for line in text_content.splitlines(True)]
    with codecs.open(output_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
        #f.writelines(output_lines)


def download_page(url):
    """ Take URL; return text of downloaded page. """
    # If encoding not specified in headers, this may be very slow
    # as requests invokes chardet.
    return requests.get(url).text


def tidy_html_content(content):
    """ Take content; remove multiple line breaks, return cleaned HTML. """
    return clean_html(root)


def process_page(filename, url):
    """ Process a page; download it, save output. """
    html = download_page(url)
    write_output(filename, clean_html(html))

    
def main():
    """ Read HTML file and output cleaned text from it. """
    content = read_file(sys.argv[1])
    cleaned_html = clean_html(content)
    write_output(sys.argv[2], cleaned_html)


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
