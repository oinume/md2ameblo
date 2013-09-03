# -*- coding: utf-8 -*-
from bottle import redirect, request
from md2ameblo.webapp import app, template
from md2ameblo.core import BlogKind, Markdown2Blogger

@app.route('/blogger')
def index():
    return template(
        'index.html',
        blog_kind = 'blogger',
        blog_kind_text = BlogKind.text('blogger')
    )

