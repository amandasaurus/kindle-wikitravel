#! /usr/bin/env python

import requests, sys, lxml.html

title = sys.argv[1]

initial_url = "http://wikitravel.org/wiki/en/index.php?title={0}&printable=yes".format(title)
data = requests.get(initial_url)

root = lxml.html.fromstring(data.content)
directory_structure = root.cssselect("span.subpages")[0].text_content()


urls_link_here = {x.attrib['href'] for x in root.cssselect("a") if 'href' in x.attrib}
other_pages = {url for url in urls_link_here if url.startswith("/en/") and not any(url.startswith("/en/{0}".format(x)) for x in ['Special:', 'Wikitravel:', 'File:', 'Category:', 'Talk:', 'Main_Page'])}
print other_pages
import pdb ; pdb.set_trace()

urls_to_download = set()
urls_looked_at = {initial_url}

while len(urls_looked_at) > 0:
    pass


