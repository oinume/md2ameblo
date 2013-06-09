import os

initializea = ''

config_common = {
    'debug': False,
    'reloader': False,
}
config_development = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'reloader': True,
    'server': 'wsgiref',
#    'server': 'gunicorn',
#    'workers': 1,
}
config_testing = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'reloader': True,
    'server': 'gunicorn',
}
config_production = {
    'host': '0.0.0.0',
    'port': 8081,
    'debug': False,
    'reloader': False,
    'server': 'gunicorn',
    'workers': 1,
}

mode = os.environ.get('MD2AMEBLO_ENV', 'development')
config_env = None
if mode == 'development':
    config_env = config_development
elif mode == 'testing':
    config_env = config_testing
elif mode == 'production':
    config_env = config_production
else:
    raise ValueError("Unknown config mode: " + mode)

config = dict(config_common.items() + config_env.items())

