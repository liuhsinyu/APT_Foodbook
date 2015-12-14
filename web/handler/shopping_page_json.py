import os
import urllib
import time
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from recipe import Recipe,Photo,User,Save_cache
from main_page import BaseHandler
from webapp2_extras import sessions

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class ShoppingPage_JSON(BaseHandler):
    def get(self):
        user = User.get_by_id(self.request.get('user_id'))

        shopping_dict = []
        for item in user.shopping_list:
            item_dict = {'todoText':item, 'done':False}
            shopping_dict.append(item_dict)

        json_dict = {"item":[]}

        if len(user.shopping_list) != 0:
            for item in user.shopping_list:
                json_dict['item'].append(item)
        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)


