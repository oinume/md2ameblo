# -*- coding: utf-8 -*-
import os
import sys
def set_sys_path(file):
    parent, bin_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent)

set_sys_path(__file__)
#print sys.path

from bottle import run
from md2ameblo.webapp import app
from md2ameblo.config import config
from md2ameblo.view import index

if __name__ == '__main__':
    app.log.debug("config = %s" % app.config)
    #app.log.debug("routes = %s" % app.routes)
    if app.config['debug']:
        routes_debug = ''
        # TODO: 関数が定義されているファイル名も表示する
        import inspect
        for route in app.routes:
            routes_debug += "%6s %s\n" % (route.method, route.rule)
        #self.router.add(route.rule, route.method, route, name=route.name)
        #inspect.getargspec(func)
        app.log.debug("===== routes =====\n" + routes_debug)

    port = os.environ.get('PORT')
    if port:
        config['port'] = port
    run(app, **config)
