#! /usr/bin/env python

import requests, sys, lxml.html

title = sys.argv[1]

data = requests.get("http://wikitravel.org/wiki/en/index.php?title={0}&printable=yes".format(title))

import pdb ; pdb.set_trace()
root = lxml.html.fromstring(data)
directory_structure = root.cssselect("span.subpages")[0].text_content()
