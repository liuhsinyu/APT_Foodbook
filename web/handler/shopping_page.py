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

class ShoppingPage(BaseHandler):
    def get(self):
        user = User.get_by_id(self.session.get('user_id'))
        print self.session.get('user_id')
        print user.shopping_list
        print type(user.shopping_list)
        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)
        shopping_dict = []
        for item in user.shopping_list:
            item_dict = {'todoText':item, 'done':False}
            shopping_dict.append(item_dict)
        tmp_recipes_list = []
        for recipe_id in user.tmp_recipes:
            recipe = Recipe.get_by_id(long(recipe_id))
            recipe_dict = {'photo':'http://placehold.it/700x400',
                           'name':recipe.name,
                           'tags':recipe.tags,
                           'id':str(recipe.key.id()),
                           }
            if len(recipe.photos)>0:
                recipe_dict['photo'] = images.get_serving_url(recipe.photos[0].blob_key)
            tmp_recipes_list.append(recipe_dict)
        template = JINJA_ENVIRONMENT.get_template('template/shopping_page.html')
        template_values = {
            'shopping_dict':json.dumps(shopping_dict),
            'tmp_recipes':tmp_recipes_list,
            'keywords':json.dumps(save_cache.save_cache),
        }
        self.response.write(template.render(template_values))

class AddItemShoppingList(BaseHandler):
    def post(self):
        user = User.get_by_id(self.session.get('user_id'))
        if self.request.get("newItem")!="":
            newItem = self.request.get("newItem")
            user.shopping_list.append(newItem)
            user.put()
            time.sleep(0.5)
        elif self.request.get("shoppingList")!="":
            shoppingList = [ item["todoText"] for item in json.loads(self.request.get("shoppingList"))]
            user.shopping_list = shoppingList
            for recipe_id in user.tmp_recipes:
                recipe = Recipe.get_by_id(long(recipe_id))
                isInRecipe = False
                for ingredient in recipe.ingredients:
                    if ingredient in user.shopping_list:
                        isInRecipe = True
                if not isInRecipe:
                    user.tmp_recipes.remove(recipe_id)
            user.put()
            time.sleep(0.5)
        self.redirect('/shoppingpage')