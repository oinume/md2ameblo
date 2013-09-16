# -*- coding: utf-8 -*-
from bottle import redirect, request
from md2ameblo.webapp import app, template
from md2ameblo.core import BlogKind, Markdown2Ameblo, Markdown2Blogger

@app.route('/')
def index():
    return template(
        'index.html',
        blog_kind = 'ameblo',
        blog_kind_text = BlogKind.text('ameblo')
    )

@app.route('/ameblo')
def index():
    return template(
        'form.html',
        blog_kind = 'ameblo',
        blog_kind_text = BlogKind.text('ameblo')
    )

@app.route('/blogger')
def index():
    return template(
        'form.html',
        blog_kind = 'blogger',
        blog_kind_text = BlogKind.text('blogger')
    )

@app.route('/process', method='POST')
def process():
    source = request.params.source
    #app.log.debug("parser = %s, converter = %s, prefer_h1 = %s" % (sparser, sconverter, prefer_h1))
    if not source:
        return redirect('/')

    #s = source.decode('utf-8')
    #app.log.debug("===== source =====\n" + source)

    blog_kind = request.params.blog_kind
    if blog_kind == 'ameblo':
        md2html = Markdown2Ameblo(app.log)
    else:
        md2html = Markdown2Blogger(app.log)

    converted_value = md2html.convert(source)
    return template(
        'complete.html',
        converted_value=converted_value,
        blog_kind = blog_kind,
        blog_kind_text = BlogKind.text(blog_kind)
    )

@app.route('/complete')
def complete():
    pass
