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

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class ViewPage(BaseHandler):
    def get(self):
        recipe_id = self.request.get('recipe_id')
        print "-------------------"
        recipe = Recipe.get_by_id(long(recipe_id))

        recipe_query = History.query(History.recipe_authorID==self.session.get('user_id'))
        recipe_query_test = recipe_query.fetch()
        print recipe_query_test
        print 'yoyoyoyoyo'

        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)
        photo_urls = []
        for i in xrange(len(recipe.photos)):
            photo_urls.append(images.get_serving_url(recipe.photos[i].blob_key))
        author = User.get_by_id(recipe.author)
        ingredients_list = []
        user = User.get_by_id(self.session.get('user_id'))
        shopping_list = user.shopping_list
        isAllInList = True
        for ingredient in recipe.ingredients:
            if ingredient in shopping_list:
                ingredients_list.append((ingredient,True))
            else:
                ingredients_list.append((ingredient,False))
                isAllInList = False
        isAuthor = False
        if user.user_id == author.user_id:
            isAuthor = True
        isFavorite = False
        if recipe_id in user.favorite_recipes:
            isFavorite = True
        isWish = False
        if recipe_id in user.wish_recipes:
            isWish = True
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
        template = JINJA_ENVIRONMENT.get_template('template/view_page.html')
        template_values = {
            'recipe_id':recipe_id,
            'recipe_name':recipe.name,
            'keywords':json.dumps(save_cache.save_cache),
            'photo_urls':photo_urls,
            'author':author.user_name,
            'ingredients':ingredients_list,
            'directions':recipe.directions,
            'estimate_time':recipe.estimate_time,
            'portion':recipe.portion,
            'tags':recipe.tags,
            'isAllInList':isAllInList,
            'isFavorite':isFavorite,
            'isWish':isWish,
            'isAuthor':isAuthor,
            'comments_list':comments_list,
            'same_list':same_list,
            'same_list_len':len(same_list),
        }
        self.response.write(template.render(template_values))

class EditPage(BaseHandler):
    def get(self):
        recipe_id = self.request.get('recipe_id')
        recipe = Recipe.get_by_id(long(recipe_id))
        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)
        photo_urls = []
        for i in xrange(len(recipe.photos)):
            photo_urls.append(images.get_serving_url(recipe.photos[0].blob_key))
        user = User.get_by_id(self.session.get('user_id'))

        template = JINJA_ENVIRONMENT.get_template('template/edit_page.html')
        template_values = {
            'recipe_id':recipe_id,
            'recipe_name':recipe.name,
            'photo_urls':photo_urls,
            'author':user.user_name,
            'description':recipe.description,
            'ingredients':recipe.ingredients,
            'directions':recipe.directions,
            'estimate_time':recipe.estimate_time.strftime('%H:%M'),
            'portion':recipe.portion,
            'tags':json.dumps(recipe.tags),
            'keywords':json.dumps(save_cache.save_cache),
        }
        self.response.write(template.render(template_values))

class ModifyRecipe(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        name = self.request.get('recipe_name')
        author = self.request.get('user_id')

        recipe_query = Recipe.query(Recipe.name == name,Recipe.author == author)
        recipes = recipe_query.fetch(1)
        if len(recipes) >0:
            recipe = recipes[0]
        else:
            recipe = Recipe()
            recipe.favorite_count = 0
            recipe.view_count = 0
            recipe.name = name
            recipe.author = author
            recipe_query = Recipe.query(Recipe.name==name)
            recipes = recipe_query.fetch(1)
            recipe.photos = recipes[0].photos

        if self.request.get('estimated_time') != "":
            tmp = time.strptime(self.request.get('estimated_time'),"%H:%M")
            recipe.estimate_time = datetime.time(hour=tmp.tm_hour,minute=tmp.tm_min)
        else:
            recipe.estimate_time =datetime.time(hour=0,minute=0)
        recipe.portion = int(self.request.get('portions'))
        recipe.description = self.request.get('description')

        recipe.ingredients = []
        ingredient_number = int(self.request.get('ingredient_number'))
        for i in xrange(ingredient_number):
            if self.request.get('ingredient'+str(i+1))!="":
                recipe.ingredients.append(self.request.get('ingredient'+str(i+1)))

        recipe.directions = []
        direction_number = int(self.request.get('direction_number'))
        for i in xrange(direction_number):
            if self.request.get('direction'+str(i+1))!="":
                recipe.directions.append(self.request.get('direction'+str(i+1)))
        if self.request.get('tag[]')!="":
            recipe.tags = json.loads(self.request.get('tag[]'))

        recipe.put()
        time.sleep(1)
        self.redirect('/viewpage?recipe_id='+str(recipe.key.id()))


class AddShoppingList(BaseHandler):
    def get(self):
        recipe_id = self.request.get('recipe_id')
        ingredient_idx = int(self.request.get('ingredient_idx'))-1
        if self.request.get('add') == 'true':
            isAdd = True
        else:
            isAdd = False
        user_id = self.session.get('user_id')
        recipe = Recipe.get_by_id(long(recipe_id))
        user = User.get_by_id(self.session.get('user_id'))
        if ingredient_idx < 0:
            if isAdd:
                if recipe_id not in user.tmp_recipes:
                    user.tmp_recipes.append(recipe_id)
                for ingredient in recipe.ingredients:
                    if ingredient not in user.shopping_list:
                        user.shopping_list.append(ingredient)
            else:
                for ingredient in recipe.ingredients:
                    user.shopping_list.remove(ingredient)
                if recipe_id in user.tmp_recipes:
                    user.tmp_recipes.remove(recipe_id)
        else:
            if isAdd:
                if recipe_id not in user.tmp_recipes:
                    user.tmp_recipes.append(recipe_id)
                if recipe.ingredients[ingredient_idx] not in user.shopping_list:
                    user.shopping_list.append(recipe.ingredients[ingredient_idx])
            else:
                user.shopping_list.remove(recipe.ingredients[ingredient_idx])
                isInRecipe = False
                for ingredient in recipe.ingredients:
                    if ingredient in user.shopping_list:
                        isInRecipe = True
                if not isInRecipe:
                    user.tmp_recipes.remove(recipe_id)
        user.put()
        time.sleep(0.5)
        self.redirect('viewpage?recipe_id='+str(recipe_id))

class AddToBox(BaseHandler):
    def get(self):
        recipe_id = self.request.get('recipe_id')
        type = self.request.get('type')
        value = self.request.get('value')
        user = User.get_by_id(self.session.get('user_id'))
        if type=="favorite":
            if value == "true":
                user.favorite_recipes.append(recipe_id)
            else:
                user.favorite_recipes.remove(recipe_id)
        elif type=="wish":
            if value == "true":
                user.wish_recipes.append(recipe_id)
            else:
                user.wish_recipes.remove(recipe_id)
        user.put()
        time.sleep(0.5)
        self.redirect('viewpage?recipe_id='+str(recipe_id))

class WriteComment(BaseHandler):
    def post(self):
        recipe_id = self.request.get('recipe_id')
        recipe = Recipe.get_by_id(long(recipe_id))
        if self.request.get('comment')!="":
            user = User.get_by_id(self.session.get('user_id'))
            comment = Comment(author=user.user_id,comment_text=self.request.get('comment'))
            recipe.comments.append(comment)
            recipe.put()
            time.sleep(1)
        self.redirect('viewpage?recipe_id='+str(recipe_id))
