from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
    """Sub model for representing an author."""
    user_id = ndb.StringProperty(indexed=True)
    user_name = ndb.StringProperty(indexed=True)
    friends = ndb.StringProperty(repeated=True)
    photo = ndb.StringProperty()
    shopping_list = ndb.StringProperty(repeated=True,indexed=False)
    tmp_recipes = ndb.StringProperty(repeated=True)
    favorite_recipes = ndb.StringProperty(repeated=True)
    wish_recipes = ndb.StringProperty(repeated=True)
    my_recipes = ndb.StringProperty(repeated=True)

class Photo(ndb.Model):
    filename = ndb.StringProperty()
    author = ndb.StringProperty(indexed=True)
    upload_time = ndb.DateTimeProperty(auto_now_add=True)
    blob_key = ndb.BlobKeyProperty()

class Comment(ndb.Model):
    author = ndb.StringProperty(indexed=True)
    comment_text = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class Recipe(ndb.Model):
    name = ndb.StringProperty()
    author = ndb.StringProperty(indexed=True)
    photos = ndb.StructuredProperty(Photo,repeated=True)
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    estimate_time = ndb.TimeProperty()
    description = ndb.StringProperty()
    portion = ndb.IntegerProperty(indexed=False)
    ingredients = ndb.StringProperty(repeated=True,indexed=False)
    directions = ndb.StringProperty(repeated=True,indexed=False)
    tags = ndb.StringProperty(repeated=True)
    view_count = ndb.IntegerProperty(indexed=False)
    favorite_count = ndb.IntegerProperty(indexed=False)
    comments = ndb.StructuredProperty(Comment,repeated=True)

class Save_cache(ndb.Model):
    save_cache = ndb.GenericProperty(repeated=True)

class History(ndb.Model):
    recipe_author = ndb.StringProperty(indexed=True)
    author_comments = ndb.StringProperty()
    recipe_id = ndb.StringProperty()
    recipe_authorID = ndb.StringProperty(indexed=True)
    recipe_name = ndb.StringProperty()
    FromAndroid = ndb.BooleanProperty()
    photos = ndb.StructuredProperty(Photo,repeated=True)
    tags = ndb.StringProperty(repeated=True)
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    recipe_description = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comment,repeated=True)
    comments_author = ndb.StructuredProperty(Comment,repeated=True)