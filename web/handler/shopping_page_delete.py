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


class ShoppingPage_Delete(webapp2.RequestHandler):
    def post(self):
        user = User.get_by_id(self.request.get('user_id'))

        shoppingList = []
        if self.request.get("DeleteItem")!="":
            DeleteItem = self.request.get("DeleteItem")
            delete_item_list = DeleteItem.split(',')
            for i in xrange(len(user.shopping_list)):
                if str(i) not in delete_item_list:
                    shoppingList.append(user.shopping_list[i])

        for recipe_id in user.tmp_recipes:
                recipe = Recipe.get_by_id(long(recipe_id))
                isInRecipe = False
                for ingredient in recipe.ingredients:
                    if ingredient in shoppingList:
                        isInRecipe = True
                if not isInRecipe:
                    user.tmp_recipes.remove(recipe_id)


        user.shopping_list = shoppingList
        user.put()
        time.sleep(0.5)

        self.redirect('/shoppingpage')
