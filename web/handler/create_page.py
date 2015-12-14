import os
import urllib
import time
import datetime

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from recipe import Recipe,Photo,User,Save_cache,History

import jinja2
import webapp2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_Save_Cache_NAME = 'default_save_cache'

class CreatePage(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/createrecipe')
        upload_url = str(upload_url)
        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if not save_cache:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        print upload_url
        template = JINJA_ENVIRONMENT.get_template('template/create_page.html')
        template_values = {
            'upload_url':upload_url,
            'keywords':json.dumps(save_cache.save_cache),
        }
        self.response.write(template.render(template_values))

class CreateRecipe(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads('cover_image')
        name = self.request.get('recipe_name')
        author = self.request.get('user_id')
        recipe_query = Recipe.query(Recipe.name == name,Recipe.author == author)
        recipes = recipe_query.fetch(1)
        if len(recipes) >0:
            self.error(409)
            self.redirect('/error?error=1')
        else:
            recipe = Recipe()

            recipe.name = name
            if self.request.get('estimated_time') != "":
                tmp = time.strptime(self.request.get('estimated_time'),"%H:%M")
                recipe.estimate_time = datetime.time(hour=tmp.tm_hour,minute=tmp.tm_min)
            else:
                recipe.estimate_time =datetime.time(hour=0,minute=0)
            recipe.portion = int(self.request.get('portions'))
            recipe.description = self.request.get('description')

            ingredient_number = int(self.request.get('ingredient_number'))
            for i in xrange(ingredient_number):
                if self.request.get('ingredient'+str(i+1))!="":
                    recipe.ingredients.append(self.request.get('ingredient'+str(i+1)))

            direction_number = int(self.request.get('direction_number'))
            for i in xrange(direction_number):
                if self.request.get('direction'+str(i+1))!="":
                    recipe.directions.append(self.request.get('direction'+str(i+1)))
            if self.request.get('tag[]')!="":
                recipe.tags = json.loads(self.request.get('tag[]'))

            recipe.favorite_count = 0
            recipe.view_count = 0
            if len(upload) >0:
                recipe.photos.append(Photo(
                    blob_key = upload[0].key(),
                    filename= upload[0].filename,
                ))
            recipe.author = author

            recipe.put()
            history = History()
            history.recipe_name = name
            history.FromAndroid = False
            history.recipe_id = str(recipe.key.id())
            history.tags = json.loads(self.request.get('tag[]'))
            history.recipe_author=User.get_by_id(author).user_name
            history.recipe_description= self.request.get('description')
            history.recipe_authorID = author
            if len(upload) >0:
                history.photos.append(Photo(
                    blob_key = upload[0].key(),
                    filename= upload[0].filename,
                ))
            history.put()
            print history

            time.sleep(1)
            self.redirect('/viewpage?recipe_id='+str(recipe.key.id()))
