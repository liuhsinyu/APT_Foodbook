import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from handler.main_page import MainPage,LoginPage
from handler.create_page import CreatePage,CreateRecipe
from handler.view_page import ViewPage,EditPage,AddShoppingList,ModifyRecipe,AddToBox,WriteComment
from handler.view_page_json import ViewPage_JSON,UploadPhoto_json,GetUploadURL
from handler.recipe_box import RecipeBox
from handler.save_cache import savecache
from handler.timeline import Timeline,WriteComment_Intimeline
from handler.recipe_box_json import RecipeBox_JSON
from handler.search_recipe import search_recipe,search_recipes
from handler.shopping_page import ShoppingPage,AddItemShoppingList
from handler.shopping_page_json import ShoppingPage_JSON
from handler.shopping_page_add import ShoppingPage_Add
from handler.shopping_page_delete import ShoppingPage_Delete
from handler.error_page import ErrorPage

import jinja2
import webapp2

DEFAULT_STREAM_NAME = 'default_stream'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/createpage', CreatePage),
    ('/createrecipe', CreateRecipe),
    ('/viewpage', ViewPage),
    ('/viewpage_json', ViewPage_JSON),
    ('/recipebox_json', RecipeBox_JSON),
    ('/savecache',savecache),
    ('/editpage', EditPage),
    ('/recipebox',RecipeBox),
    ('/search_recipe',search_recipe),
    ('/search_recipes',search_recipes),
    ('/writecomment',WriteComment),
    ('/writecomment_intimeline',WriteComment_Intimeline),
    ('/editpage', EditPage),
    ('/uploadphoto_json',UploadPhoto_json),
    ('/uploadHandler',GetUploadURL),
    ('/recipebox',RecipeBox),
    ('/timeline',Timeline),
    ('/addshoplist',AddShoppingList),
    ('/modifyrecipe',ModifyRecipe),
    ('/shoppingpage',ShoppingPage),
    ('/shoppingpage_json',ShoppingPage_JSON),
    ('/shoppingpage_add',ShoppingPage_Add),
    ('/shoppingpage_delete',ShoppingPage_Delete),
    ('/additemshoppinglist',AddItemShoppingList),
    ('/addtobox',AddToBox),
    ('/error',ErrorPage),
], config=config,debug=True)