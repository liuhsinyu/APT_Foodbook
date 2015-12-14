import os
import urllib
import time
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from recipe import Recipe,Photo,User,Comment,Save_cache,History
from main_page import BaseHandler

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ViewPage_JSON(BaseHandler):
    def get(self):
        recipe_id = self.request.get('recipe_id')
        recipe = Recipe.get_by_id(long(recipe_id))

        photo_urls = []
        for i in xrange(len(recipe.photos)):
            photo_urls.append(images.get_serving_url(recipe.photos[0].blob_key))
        author = User.get_by_id(recipe.author)
        ingredients_list = []
        # user = User.get_by_id(self.session.get('user_id'))
        # shopping_list = user.shopping_list
        # isAllInList = True
        for ingredient in recipe.ingredients:
            ingredients_list.append(ingredient)

        # isAuthor = False
        # if user.user_id == author.user_id:
        #     isAuthor = True
        # isFavorite = False
        # if recipe_id in user.favorite_recipes:
        #     isFavorite = True
        # isWish = False
        # if recipe_id in user.wish_recipes:
        #     isWish = True
        comments_list = []
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

        same_list = []
        recipe_name = Recipe.query(Recipe.name==recipe.name)
        for recipe2 in recipe_name:
            if User.get_by_id(recipe2.author).user_name is not author.user_name:
                same_dict = {
                    'author': User.get_by_id(recipe2.author).user_name,
                    'recipe_id': recipe2.key.id(),
                }
                same_list.append(same_dict)
        print author.user_name
        # template = JINJA_ENVIRONMENT.get_template('template/view_page.html')
        # template_values = {
        #     'recipe_id':recipe_id,
        #     'recipe_name':recipe.name,
        #     'photo_urls':photo_urls,
        #     'author':author.user_name,
        #     'ingredients':ingredients_list,
        #     'directions':recipe.directions,
        #     'estimate_time':recipe.estimate_time,
        #     'portion':recipe.portion,
        #     'tags':recipe.tags,
        #     'isAllInList':isAllInList,
        #     'isFavorite':isFavorite,
        #     'isWish':isWish,
        #     'isAuthor':isAuthor,
        #     'comments_list':comments_list,
        #     'same_list':same_list,
        # }
        # self.response.write(template.render(template_values))

        json_dict = {"recipe_id":[],"recipe_name":[],"photo_urls":[],"author":[],"ingredients":[],"directions":[],"estimate_time":[],"portion":[],"tags":[],"isAllInList":[],"isFavorite":[],"isWish":[],"isAuthor":[],"comments_list":[],"same_list":[]}
        json_dict['recipe_id'] = recipe_id
        json_dict['recipe_name'] = recipe.name
        json_dict['photo_urls'] = photo_urls[0]
        json_dict['author'] = author.user_name
        json_dict['ingredients'] = ingredients_list
        json_dict['directions'] =recipe.directions
        json_dict['estimate_time']=recipe.estimate_time.strftime("%H:%M")
        json_dict['portion'] = recipe.portion
        json_dict['tags']= recipe.tags
        # json_dict['isAllInList']= isAllInList
        # json_dict['isFavorite'] =isFavorite
        # json_dict['isWish'] = isWish
        # json_dict['isAuthor'] = isAuthor
        json_dict['comments_list'] = comments_list
        json_dict['same_list'] = same_list
        jsonObj = json.dumps(json_dict, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)


class GetUploadURL(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/uploadphoto_json')
        upload_url = str(upload_url)
        dictPassed = {'upload_url':upload_url}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

class UploadPhoto_json(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        recipe_id = self.request.get('recipe_id')
        recipe = Recipe.get_by_id(long(recipe_id))
        # # user_id = self.session.get('user_id')
        author_comments = self.request.get('author_comments')
        user_id = self.request.get('user_id')
        user = User.get_by_id(user_id)

        #img = images.resize(img, 200, 200)
        # if len(upload) >0:
        #     recipe.photos.append(Photo(
        #     blob_key = upload[0].key(),
        #     filename= upload[0].filename,
        # ))
        recipe.put()

        history = History()
        history.recipe_name = recipe.name
        history.author_comments = author_comments
        history.FromAndroid = True
        history.recipe_id = str(recipe.key.id())
        history.tags = recipe.tags
        history.recipe_author= user.user_name
        history.recipe_description= recipe.description
        history.recipe_authorID = user_id

        history.photos.append(Photo(
            blob_key = upload.key(),
            filename= "hi",
        ))
        # if len(upload) >0:
        #     history.photos.append(Photo(
        #         # blob_key = upload[0].key(),
        #         # filename= upload[0].filename,
        #         blob_key = upload.key(),
        #         filename= "hi",
        #     ))
        history.put()
        time.sleep(1)