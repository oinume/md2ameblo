# -*- coding: utf-8 -*-

import re
from HTMLParser import HTMLParser
import misaka

class AmebloHtmlRenderer(misaka.HtmlRenderer, misaka.SmartyPants):
    def block_code(self, text, lang):
        s = ''
        if not lang:
            lang = 'text'
        # コンソール系とソースコードで色付けを変える
        if lang in [ 'sh', 'bash', 'zsh' ]:
            s = '<pre style="background-color:#444;color:#0f0;white-space:pre-wrap;word-wrap:break-word;padding:4px;">%s</pre>' % (text)
        else:
            s = '<pre style="border:solid #666 1px;background-color:#fff;white-space:pre-wrap;word-wrap:break-word;padding:4px;">%s</pre>' % (text)
        return s

class Markdown2Ameblo(object):
    def __init__(self, log):
        self._log = log

    def convert(self, markdown_text, **options):
        markdown = misaka.Markdown(
            AmebloHtmlRenderer(flags = misaka.HTML_HARD_WRAP | misaka.HTML_SAFELINK),
            extensions = misaka.EXT_FENCED_CODE
            | misaka.EXT_NO_INTRA_EMPHASIS
            | misaka.EXT_TABLES
            | misaka.EXT_AUTOLINK
            | misaka.EXT_SPACE_HEADERS
            | misaka.EXT_STRIKETHROUGH
            | misaka.EXT_SUPERSCRIPT)
        html = markdown.render(markdown_text)
        self._log.debug("--- html ---\n" + html)
        html_parser = AmebloHTMLParser(self._log, **options)
        html_parser.feed(html)
        print html_parser.converted_html()
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
        self._log.debug("start tag: '%s'" % (tag))
        if self._in_pre:
            self._converted_html += self.escape_html(self.convert_tag(tag, True, attrs))
        else:
            self._converted_html += self.convert_tag(tag, True, attrs)
        if tag in [ "pre" ]:
            self._in_pre = True

    def handle_endtag(self, tag):
        if tag in [ "pre" ]:
            self._in_pre = False
        self._log.debug("end tag: '%s'" % (tag))
        if self._in_pre:
            self._converted_html += self.escape_html(self.convert_tag(tag, False))
        else:
            self._converted_html += self.convert_tag(tag, False)

    def handle_data(self, data):
        self._log.debug("data: '%s'" % (self.escape(data)))
        if self._in_pre:
            self._converted_html += self.escape_html(data)
        else:
            if re.match(r"^\s*$", data):
                self._log.debug("Ignored.")
                return
            self._converted_html += data.strip()

    def convert_tag(self, tag, start, attrs = {}):
        #map = { "code": "pre", "h1": "h3", "h2": "h3" }
        mappings = { "h1": "h3", "h2": "h3" }
        element = mappings.get(tag, tag)
        self._log.debug("attrs:" + str(attrs))
        if start:
            if len(attrs) == 0:
                return "<%s>" % (element)
            else:
                tag = "<%s" % (element)
                for attr in attrs:
                    tag += ' %s="%s"' % (attr[0], attr[1])
                tag += ">"
                return tag
        else:
            return "</%s>" % (element)

    def converted_html(self):
        html = self._converted_html
        html = re.sub(r"<pre>\s+", "<pre>", html)
        html = re.sub(r"\s+</pre>", "</pre>", html)
        return html

    def escape(self, text):
        mappings = { "\r": "\\r", "\n" : "\\n", "\t": "\\t" }
        ret = ''
        for char in text:
            if mappings.get(char):
                ret += mappings[char]
            else:
                ret += char
        return ret

    def escape_html(self, text):
        escaped = ''
        for char in text:
            if char == '<':
                escaped += '&amp;lt;'
            elif char == '>':
                escaped += '&amp;gt;'
            elif char == '&':
                escaped += '&amp;'
            elif char == '"':
                escaped += '&amp;quot;'
            else:
                escaped += char
        return escaped

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
