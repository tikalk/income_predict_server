#! /usr/bin/env python
import os
import ConfigParser
from flask import Flask
import logging.config


def configure_logging():
#    print 'Configuring logging'
    try:
        logging_conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './conf/logging.conf')
        logging.config.fileConfig(logging_conf_path)
    except BaseException, e:
        logging_conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './logging.conf')
        logging.config.fileConfig(logging_conf_path)

    log = logging.getLogger('app')
#    log.warn("Init logging")
    return log

def get_config():
    config = ConfigParser.SafeConfigParser()
    default_ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './conf/localhost.ini')
    ini_path = os.environ.get('CONF_INI_PATH', default_ini_path)
    config.read(ini_path)
    return config

def _env_lookup(key, default=None):
    prop = os.environ.get(key)
    if not prop:
        prop = os.environ.get(key.upper(), default)
    return prop

def get_app():
    app = Flask(__name__)
    # CORS(app)
    return app


# conf = get_config()
# log = configure_logging()
# server = Flask(__name__)
# CORS(server)