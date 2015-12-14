import os
import urllib
import time
import datetime

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from recipe import Recipe,Photo,User,Save_cache

import jinja2
import webapp2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class search_recipe(webapp2.RequestHandler):
    def post(self):

        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        recipe_query_tag = ()


        stream_merge_list =[]
        if self.request.get('search_tag') != "":
            search_tag = self.request.get('search_tag')
            stream__tag = Recipe.query(Recipe.tags==search_tag)
            stream_query_tag = stream__tag.fetch()
            stream__name = Recipe.query(Recipe.name==search_tag)
            stream_query_name = stream__name.fetch()
            stream_merge = stream_query_name+stream_query_tag
            stream_merge_list = []
            seen = set()
            for item in stream_merge:
                if item.key.id() not in seen:
                    stream_merge_list.append(item)
                    seen.add(item.key.id())

            for test in stream_merge_list:
                print test.name
            print '---------------'
            print type(stream_merge)
            print search_tag

            if len(stream_merge_list)>8:
                stream_merge_list = stream_merge_list[0:8]

        # json_dict = {"photo_urls":[],"Recipe_id":[],"Recipe_name":[]}
        # for recipe in stream_merge_list:
        #     json_dict['photo_urls'].append(images.get_serving_url(recipe.photos[0].blob_key))
        #     json_dict['Recipe_id'].append(recipe.key.id())
        #     json_dict['Recipe_name'].append(recipe.name)
        #     print recipe.key.id()
        #     print images.get_serving_url(recipe.photos[0].blob_key)
        #
        # print type(json_dict)
        # print json_dict

        recipe_list = []
        for recipe in stream_merge_list:
            json_dict = {}
            json_dict['photo_urls'] = images.get_serving_url(recipe.photos[0].blob_key)
            json_dict['Recipe_id'] = recipe.key.id()
            json_dict['Recipe_name'] = recipe.name
            json_dict['Author'] = User.get_by_id(recipe.author).user_name
            print recipe.key.id()
            print images.get_serving_url(recipe.photos[0].blob_key)
            recipe_list.append(json_dict)
        print type(json_dict)
        print json_dict

        # for recipe in json_dict:
        #     print "hi"
        #     print recipe['photo_urls']

        #keywords = dict(zip(['term'], [keywords_list]))


        template_values = {
            'streams_search': stream_merge_list,
            'search_tag': search_tag,
            'num_search': len(stream_merge_list),
            'recipe_list': recipe_list,
            'keywords':json.dumps(save_cache.save_cache),
        }

        template = JINJA_ENVIRONMENT.get_template('template/search_page.html')
        self.response.write(template.render(template_values))


class search_recipes(webapp2.RequestHandler):
    def get(self):

        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        recipe_query_tag = ()


        stream_merge_list =[]
        if self.request.get('search_tag') != "":
            search_tag = self.request.get('search_tag')
            stream__tag = Recipe.query(Recipe.tags==search_tag)
            stream_query_tag = stream__tag.fetch()
            stream__name = Recipe.query(Recipe.name==search_tag)
            stream_query_name = stream__name.fetch()
            stream_merge = stream_query_name+stream_query_tag
            stream_merge_list = []
            seen = set()
            for item in stream_merge:
                if item.key.id() not in seen:
                    stream_merge_list.append(item)
                    seen.add(item.key.id())

            for test in stream_merge_list:
                print test.name
            print '---------------'
            print type(stream_merge)
            print search_tag

            if len(stream_merge_list)>8:
                stream_merge_list = stream_merge_list[0:8]

        # json_dict = {"photo_urls":[],"Recipe_id":[],"Recipe_name":[]}
        # for recipe in stream_merge_list:
        #     json_dict['photo_urls'].append(images.get_serving_url(recipe.photos[0].blob_key))
        #     json_dict['Recipe_id'].append(recipe.key.id())
        #     json_dict['Recipe_name'].append(recipe.name)
        #     print recipe.key.id()
        #     print images.get_serving_url(recipe.photos[0].blob_key)
        #
        # print type(json_dict)
        # print json_dict

        recipe_list = []
        for recipe in stream_merge_list:
            json_dict = {}
            json_dict['photo_urls'] = images.get_serving_url(recipe.photos[0].blob_key)
            json_dict['Recipe_id'] = recipe.key.id()
            json_dict['Recipe_name'] = recipe.name
            json_dict['Author'] = User.get_by_id(recipe.author).user_name
            print recipe.key.id()
            print images.get_serving_url(recipe.photos[0].blob_key)
            recipe_list.append(json_dict)
        print type(json_dict)
        print json_dict

        # for recipe in json_dict:
        #     print "hi"
        #     print recipe['photo_urls']

        #keywords = dict(zip(['term'], [keywords_list]))


        template_values = {
            'streams_search': stream_merge_list,
            'search_tag': search_tag,
            'num_search': len(stream_merge_list),
            'recipe_list': recipe_list,
            'keywords':json.dumps(save_cache.save_cache),
        }

        template = JINJA_ENVIRONMENT.get_template('template/search_page.html')
        self.response.write(template.render(template_values))
