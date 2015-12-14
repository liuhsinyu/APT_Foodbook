import os
import urllib
import time
import datetime

import jinja2
import webapp2
import json
from recipe import Recipe,Photo,User,Save_cache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class ErrorPage(webapp2.RequestHandler):
    def get(self):
        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        template = JINJA_ENVIRONMENT.get_template('template/error_page.html')
        error_code = self.request.get('error')
        error_msgs = {
            '1':"You tried to create a recipe whose name is the same as an existing one"
        }
        direct_page = {
            '1':'createpage'
        }
        template_values = {
            'error_msg':error_msgs[error_code],
            'direct_page':direct_page[error_code],
            'keywords':json.dumps(save_cache.save_cache),
        }
        self.response.write(template.render(template_values))