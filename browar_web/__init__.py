# -*- coding: utf-8 -*-
__version__ = '0.1'
from bottle import Bottle, TEMPLATE_PATH
from browar_web.controllers import *
TEMPLATE_PATH.append("./browar_web/views/")
import web_server
import routes
