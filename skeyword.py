#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
commandline for GWEN - GateWay Email Node
'''

from __future__ import with_statement

__author__ = "Lars Wiegman <lars@namsral.com>"
__version__ = '0.2'
__docformat__ = 'plaintext'
__license__ = 'MIT'
__copyright__ = "Copyright (c) 2009, Lars Wiegman"

import os
import sys
import time
import urllib
import json
from optparse import OptionParser
import BaseHTTPServer
from urlparse import urlparse

head = """<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" /> 
        <title>SKeyword</title>
        <link rel="search" type="application/opensearchdescription+xml" title="localhost" href="/opensearch.xml">
        <style type="text/css">
            *{margin:0;padding:0}body{font-family:"Lucida Grande",verdana,sans-serif;font-size:12px;color:#888}#wrap{width:600px;margin:40px auto}fieldset{padding:10px 20px;background-color:#fefefe;border:1px solid #ddd;margin:20px 0}legend{font-size:1.2em;text-transform:uppercase;color:#bbb;padding:0 4px}ul{margin:0:padding:0}li{font-size:1em;list-style:none;float:left;margin:6px;color:#444;background-color:#eee;padding:2px 4px 2px 0}li span.keyword{background-color:#bbb;padding:2px 4px;font-weight:700}li span.url{color:#888}form{width:400px;margin:12px auto}input[type="text"]{width:400px;border:none;font-size:14px;color:#666;padding:6px 8px;margin-bottom:5px;background:#eee;width:260px;border-radius:4px}input[type="submit"]{background:#777;border:none;font-size:14px;font-weight:700;padding:4px 12px;color:#eee;border-radius:13px;margin-left:10px}
        </style>
    </head>
    <body onload="document.getElementById('q').focus();">

    <div id="wrap">
        <fieldset>
            <legend>Search</legend>
            <form method="get" action"/">
                <input type="text" name="q" id="q">
                <input type="submit" value="search">
            </form>
        </fieldset>
        <fieldset>
            <legend>Keywords</legend>
        
"""

footer = """
        </fieldset>
        <fieldset>
            <legend>Help</legend>
            <p>- Change your browser's default search engine to: http://localhost:%(port)s/?q=%%s</p>
            <p>- To add your own search keywords, edit the keywords.json file.</p>
        </fieldset>
    </div>
    </body>
    </html>
"""

opensearchplugin = '''<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:suggestions="http://www.opensearch.org/specifications/opensearch/extensions/suggestions/1.1">
    <ShortName>localhost</ShortName>
    <Description>localhost search engine</Description>
    <InputEncoding>UTF-8</InputEncoding>
    <Url type="text/html" method="GET" template="http://%s:%s/{searchTerms}"/>
</OpenSearchDescription>'''

class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        if s.path[:4] == '/?q=' and len(s.path[4:]) > 0:
            s.send_response(301)
            p = urllib.unquote_plus(s.path[4:])
            query_list = p.split()
            if query_list[0] in keywords:
                url = keywords.get(query_list[0]) % ' '.join(query_list[1:])
            else:
                url = default_search % ' '.join(query_list)
            s.send_header("Location", url)
            s.end_headers()
        elif (s.path == '/opensearch.xml'):
            s.send_response(200)
            s.send_header("Content-type", "application/opensearchdescription+xml")
            s.end_headers()
            s.wfile.write(opensearchplugin  % (host, port))
        #elif (s.path == '/') or (s.path == '/help'):
        else:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            content = ''
            for k, v in keywords.iteritems():
                v = urlparse(v)[1]
                content += '<li><span class="keyword">%s</span> <span class="url">%s</span></li>' % (k, v)
            html = '%s<ul>%s</ul>%s' % (head, content, footer % {'port':port})
            s.wfile.write(html)
    def do_GET(s):
        s.do_HEAD()

    
def load_data(fname):
    if os.access(fname, 4):
        return json.load(open(fname, 'rb'))
    else:
        print 'Couldn\'t access the keywords.json file'
        sys.exit(1)

def run(port):
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((host, port), HttpHandler)
    print time.asctime(), "Server Starts - %s:%s" % (host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (host, port)


def main():
    global keywords
    global port
    global host
    global default_search
    default_port = 9003
    host = 'localhost'
        
    parser = OptionParser(version="SKeyword %s" % __version__)
    
    parser.add_option("-p", "--port", dest="port",
        help="port number, default %s" % default_port)
    parser.add_option("-k", "--keywords-file", dest="keywords_file",
        help="path to file containing search keywords")
    
    (options, args) = parser.parse_args()
    
    #
    if options.keywords_file:
        fname = options.keywords_file
    else:
        fname = 'keywords.json'
    
    #
    data = load_data(fname)
    keywords = data['keywords']
    if 'default_keyword' in data:
        default_search = data['default_keyword']
    else:
        default_search = 'http://www.google.com/search?ie=UTF-8&oe=UTF-8&q=%s'
    
    if options.port and int(options.port) > 1:
        port = int(options.port)
    else:
        port = default_port
    
    run(port)

if __name__ == '__main__':
    main()