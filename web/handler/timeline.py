import os
import urllib
import time
import datetime

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from recipe import Recipe,Photo,User,Save_cache,History,Comment
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

class Timeline(BaseHandler):
    def get(self):

        # recipe_query = History.query(History.recipe_authorID==self.session.get('user_id'))
        recipe_query = History.query()
        recipe_query_all_tmp = recipe_query.fetch()
        recipe_query_all= sorted(recipe_query_all_tmp, key=lambda contract: (contract.create_time.strftime("%Y-%m-%d %H:%M:%S")), reverse=True)
        print recipe_query_all

        print 'yoyoyoyoyo'

        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)



        history_list = []
        for tmp in recipe_query_all:
            if tmp.FromAndroid == False:
                FromAndroid =0
            else:
                FromAndroid =1

            if len(tmp.tags)==0:
                tmp.tags.append('Delicious')
                tmp.tags.append('YUMMY')
            print tmp.recipe_id
            # avatar = images.resize(tmp.photos[0], 32, 32)
            print type(tmp.create_time.strftime)

            if not tmp.recipe_id:
                # tmp.recipe_id = '5302669702856704'
                tmp.recipe_id = '5629499534213120'
            if not tmp.author_comments:
                tmp.author_comments = 'its good'

            recipe = Recipe.get_by_id(long(tmp.recipe_id))

            comments_list = []
            if tmp.FromAndroid == False:
                for comment in recipe.comments:
                    author2 = User.get_by_id(comment.author)
                    time_str = comment.time.strftime("%B %d, %Y at %H:%M:%S")
                    comment_dict = {
                        'author':author2.user_name,
                        'author_profile':author2.photo,
                        'comment_text':comment.comment_text,
                        'time': time_str,
                    }
                    comments_list.append(comment_dict)
            else:
                for comment in tmp.comments:
                    author2 = User.get_by_id(comment.author)
                    time_str = comment.time.strftime("%B %d, %Y at %H:%M:%S")
                    comment_dict = {
                        'author':author2.user_name,
                        'author_profile':author2.photo,
                        'comment_text':comment.comment_text,
                        'time': time_str,
                    }
                    comments_list.append(comment_dict)

            recipe_dict = {'recipe_author': tmp.recipe_author,
                           'recipe_name':  tmp.recipe_name,
                           'comments': tmp.comments,
                           'comments_author': tmp.comments_author,
                           'author_comments': tmp.author_comments,
                           'comments_list': comments_list,
                           'recipe_authorID':tmp.recipe_authorID,
                           'tags': tmp.tags,
                           'id': tmp.recipe_id,
                           'FromAndroid': FromAndroid,
                           'create_time':  tmp.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                           'user_photo': User.get_by_id(tmp.recipe_authorID).photo,
                           'photo': images.get_serving_url(tmp.photos[0].blob_key),
                           'recipe_description':  tmp.recipe_description,
                           }
            history_list.append(recipe_dict)


        template = JINJA_ENVIRONMENT.get_template('template/timeline.html')
        template_values = {
            'history_list':history_list,
            'keywords':json.dumps(save_cache.save_cache),
        }
        self.response.write(template.render(template_values))


class WriteComment_Intimeline(BaseHandler):
    def post(self):
        recipe_authorID = self.request.get('recipe_authorID')
        recipe_id = self.request.get('recipe_id')
        FromAndroid = self.request.get('FromAndroid')
        if int(FromAndroid)==0:
            recipe = Recipe.get_by_id(long(recipe_id))
            if self.request.get('comment')!="":
                user = User.get_by_id(self.session.get('user_id'))
                comment = Comment(author=user.user_id,comment_text=self.request.get('comment'))
                recipe.comments.append(comment)
                recipe.put()
                time.sleep(1)
        else:
            history_query = History.query(History.recipe_id ==recipe_id, History.recipe_authorID==recipe_authorID)
            recipe_query_all= history_query.fetch()
            if self.request.get('comment')!="":
                user = User.get_by_id(self.session.get('user_id'))
                comment = Comment(author=user.user_id,comment_text=self.request.get('comment'))
                recipe_query_all[0].comments.append(comment)
                recipe_query_all[0].put()
                time.sleep(1)
        self.redirect('/timeline')
