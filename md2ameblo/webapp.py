# -*- coding: utf-8 -*-
import os
from bottle import static_file, Bottle, TEMPLATE_PATH, jinja2_template
from md2ameblo.config import config
from md2ameblo.core.log import create_logger

app = Bottle()
app.log = create_logger(config['debug'])
app_root = os.path.dirname(os.path.abspath(__file__))
app.config['app_root'] = app_root
app.config.update(config)
TEMPLATE_PATH.append(os.path.join(app_root, 'templates'))

@app.route('/static/<file_name:re:.+>', name='static')
def serve_static(file_name):
    return static_file(file_name, root=os.path.join(app.config['app_root'], 'static'))

def template(file_path, **args):
    args.setdefault('get_url', app.get_url)
    return jinja2_template(file_path, **args)
