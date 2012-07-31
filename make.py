#! /usr/bin/env python
# encoding: utf8

import requests, sys, lxml.html

pages = {}
title = sys.argv[1]

url_format = "http://wikitravel.org/wiki/en/index.php?title={title}&printable=yes"
initial_url = url_format.format(title=title)
data = requests.get(initial_url)

root = lxml.html.fromstring(data.content)
initial_directory_structure = root.cssselect("span.subpages")[0].text_content()
pages[initial_url] = root

def get_other_pages(doc_root):

    urls_link_here = {x.attrib['href'] for x in root.cssselect("a") if 'href' in x.attrib}
    other_pages = {url[4:] for url in urls_link_here if url.startswith("/en/") and not any(url.startswith("/en/{0}".format(x)) for x in ['Special:', 'Wikitravel:', 'File:', 'Category:', 'Talk:', 'Main_Page', 'Help'])}

    urls_to_download = {url_format.format(title=url) for url in other_pages}

    return urls_to_download

urls_to_download = get_other_pages(root)
urls_looked_at = {initial_url}
urls_to_download -= urls_looked_at  # just in case

while len(urls_to_download) > 0:
    url = urls_to_download.pop()

    if url in urls_looked_at:
        continue

    urls_looked_at.add(url)

    data = requests.get(url)
    root = lxml.html.fromstring(data.content)
    directory_structure = root.cssselect("span.subpages")
    if len(directory_structure) == 0:
        print "No bread crumb navigation for ", url, " consider adding {{IsPartOf|…}"
        continue
    
    directory_structure = directory_structure[0].text_content()

    if not directory_structure.startswith(initial_directory_structure):
        #print url, " is outside"
        continue

    print url, " is inside"
    pages[url] = root

    urls_link_here = {x.attrib['href'] for x in root.cssselect("a") if 'href' in x.attrib}
    other_pages = {url for url in urls_link_here if url.startswith("/en/") and not any(url.startswith("/en/{0}".format(x)) for x in ['Special:', 'Wikitravel:', 'File:', 'Category:', 'Talk:', 'Main_Page', 'Help'])}
    urls_to_download = urls_to_download | {url_format.format(title=url[4:]) for url in other_pages}
    print "Now have ", len(urls_to_download), "pages to look at"

import pdb ; pdb.set_trace()



