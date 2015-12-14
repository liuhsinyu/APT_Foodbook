import os
import urllib
import time
import datetime

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from recipe import Recipe,Photo,User,Save_cache
from main_page import BaseHandler
from webapp2_extras import sessions

import jinja2
import webapp2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class RecipeBox_JSON(BaseHandler):
    def get(self):
        user_id = self.request.get('user_id')
        list_type = self.request.get('list_type')
        list_type_int = int(list_type)

        user = User.get_by_id(user_id)
        my_recipes_list = []
        recipe_query = Recipe.query(Recipe.author == user_id)
        my_recipes = recipe_query.fetch()
        for recipe in my_recipes:
            print recipe
            recipe_dict = {'photo':'http://placehold.it/700x400',
                           'name':recipe.name,
                           'tags':recipe.tags,
                           'id':str(recipe.key.id()),
                           }
            if len(recipe.photos)>0:
                recipe_dict['photo'] = images.get_serving_url(recipe.photos[0].blob_key)
            my_recipes_list.append(recipe_dict)

        favorite_recipes_list = []
        for recipe_id in user.favorite_recipes:
            recipe = Recipe.get_by_id(long(recipe_id))
            recipe_dict = {'photo':'http://placehold.it/700x400',
                           'name':recipe.name,
                           'tags':recipe.tags,
                           'id':str(recipe.key.id()),
                           }
            if len(recipe.photos)>0:
                recipe_dict['photo'] = images.get_serving_url(recipe.photos[0].blob_key)
            favorite_recipes_list.append(recipe_dict)
        wish_recipes_list = []

        for recipe_id in user.wish_recipes:
            recipe = Recipe.get_by_id(long(recipe_id))
            recipe_dict = {'photo':'http://placehold.it/700x400',
                           'name':recipe.name,
                           'tags':recipe.tags,
                           'id':str(recipe.key.id()),
                           }
            if len(recipe.photos)>0:
                recipe_dict['photo'] = images.get_serving_url(recipe.photos[0].blob_key)
            wish_recipes_list.append(recipe_dict)

        recipes_list = []
        if list_type_int==1:
            recipes_list = my_recipes_list
        elif list_type_int ==2:
            recipes_list = favorite_recipes_list
        else:
            recipes_list = wish_recipes_list


        json_dict = {"photo":[],"name":[],"tags":[],"id":[]}

        if len(recipes_list) != 0:
            for tmp in recipes_list:
                json_dict['photo'].append(tmp['photo'])
                json_dict['name'].append(tmp['name'])
                json_dict['tags'].append(tmp['tags'])
                json_dict['id'].append(tmp['id'])

        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

