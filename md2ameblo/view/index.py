# -*- coding: utf-8 -*-
import json
from bottle import redirect, request, response, static_file
from md2ameblo.webapp import app, template
from md2ameblo.core import BlogKind, Markdown2Ameblo, Markdown2Blogger

@app.route('/')
def index():
    return static_file('static/app/index.html', app.config['app_root'])

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
# ↑Angular化に伴い使ってない

@app.route('/<blog_kind>.json', method='POST')
def convert(blog_kind):
    markdown = request.json.get('markdown')
    #app.log.debug("parser = %s, converter = %s, prefer_h1 = %s" % (sparser, sconverter, prefer_h1))
    if not markdown:
        import exceptions
        raise exceptions.StandardError("No markdown")

    #s = source.decode('utf-8')
    app.log.debug("===== markdown =====\n" + markdown)

    #blog_kind = request.json.blog_kind
    if blog_kind == 'ameblo':
        md2html = Markdown2Ameblo(app.log)
    else:
        md2html = Markdown2Blogger(app.log)

    html = md2html.convert(markdown)
    response.content_type = 'application/json'
    return json.dumps({
        'html': html.strip(),
        'blog_kind': blog_kind,
    })
