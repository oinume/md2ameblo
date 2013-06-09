# -*- coding: utf-8 -*-
from bottle import redirect, request
from md2ameblo.webapp import app, template
from md2ameblo.core import Markdown2Ameblo

@app.route('/')
def index():
    return template(
        'index.html',
    )

@app.route('/process', method='POST')
def process():
    source = request.params.source
    #app.log.debug("parser = %s, converter = %s, prefer_h1 = %s" % (sparser, sconverter, prefer_h1))
    if not source:
        return redirect('/')

    #s = source.decode('utf-8')
    app.log.debug("===== source =====\n" + source)
    md2ameblo = Markdown2Ameblo(app.log)
    converted_value = md2ameblo.convert(source)
    return template(
        'complete.html',
        converted_value=converted_value
    )

#@app.route('/process', method='POST')
#def process():
#    source = request.params.source
#    sparser = request.params.parser or 'pukiwiki'
#    sconverter = request.params.converter or 'confluence'
#    prefer_h1 = bool(request.params.prefer_h1 or '')
#
#    app.log.debug("parser = %s, converter = %s, prefer_h1 = %s" % (sparser, sconverter, prefer_h1))
#    app.log.debug("===== source =====\n" + source)
#    if not source:
#        return redirect("/%s/%s" % (sconverter, sparser))
#
#    parser = create_parser(sparser, {}, app.log)
#    converter = create_converter(sconverter, { 'prefer_h1': prefer_h1 }, app.log)
#    parser.parse(source, converter)
#
#    return template(
#        'complete.html',
#        converter=sconverter,
#        converted_text=parser.buffer.value
#    )

@app.route('/complete')
def complete():
    pass
