# -*- coding: utf-8 -*-

import re
from markdown2 import Markdown
from HTMLParser import HTMLParser

class Markdown2Ameblo(object):
    def __init__(self, log):
        self._log = log

    def convert(self, markdown_text, **options):
        markdown = Markdown()
        html = markdown.convert(markdown_text)
        html_parser = AmebloHTMLParser(self._log, **options)
        html_parser.feed(html)
        #print html_parser.converted_html()
        #raise Exception("stop")
        return html_parser.converted_html()

class AmebloHTMLParser(HTMLParser):

    def __init__(self, log, **options):
        HTMLParser.__init__(self)
        #super(AmebloHTMLParser, self).__init__()
        self._log = log
        self._converted_html = ''
        self._in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag in [ "pre", "code" ]:
            self._in_pre = True
        self._log.debug("start tag: '%s'" % (tag))
        self._converted_html += "<%s>" % (self.convert_tag(tag))

    def handle_endtag(self, tag):
        if tag == "pre":
            self._in_pre = False
        self._log.debug("end tag: '%s'" % (tag))
        self._converted_html += "</%s>" % (self.convert_tag(tag))

    def handle_data(self, data):
        self._log.debug("data: '%s'" % (self.escape(data)))
        if self._in_pre:
            self._converted_html += data
        else:
            if re.match(r"^\s*$", data):
                self._log.debug("Ignored.")
                return
            self._converted_html += data.strip()

    def convert_tag(self, tag):
        map = { "code": "pre", "h1": "h3", "h2": "h3" }
        return map.get(tag, tag)

    def converted_html(self):
        html = self._converted_html
        html = re.sub(r"<pre>\s+", "<pre>", html)
        html = re.sub(r"\s+</pre>", "</pre>", html)
        return html

    def escape(self, text):
        map = { "\r": "\\r", "\n" : "\\n", "\t": "\\t" }
        ret = ''
        for char in text:
            if map.get(char):
                ret += map[char]
            else:
                ret += char
        return ret


#print markdown.convert("""
## h1
#hoge
#
### h2
#
#```ruby:qiita.rb
##!/usr/bin/ruby
#```
#
#### h3
#```
#```
#
#""")

# <code> -> <pre>
# 改行は<pre>の中以外は入れない
