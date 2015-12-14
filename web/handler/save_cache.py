from google.appengine.api import users
from google.appengine.ext import ndb
import os
import json
from recipe import *
import jinja2
import webapp2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_STREAM_NAME = 'default_stream'
DEFAULT_Save_Cache_NAME = 'default_save_cache'

class savecache(webapp2.RequestHandler):
    def get(self):
        print 'save ---- save ------'
        if not users.get_current_user():
            self.redirect('/')
        save_cache = Save_cache.get_by_id(DEFAULT_Save_Cache_NAME)
        if save_cache:
            print 'TEST'
        else:
            save_cache = Save_cache(id=DEFAULT_Save_Cache_NAME)

        stream_all = Recipe.query()
        stream_all_query = stream_all.fetch()
        keywords_list = []
        for tmp_stream in stream_all_query:
            if tmp_stream not in keywords_list:
                keywords_list.append(tmp_stream.name)
            if len(tmp_stream.tags)>1:
                for tag in tmp_stream.tags:
                    if tag not in keywords_list:
                        keywords_list.append(tag)
            if len(tmp_stream.tags)==1:
                if tmp_stream.tags[0] not in keywords_list:
                    keywords_list.append(tmp_stream.tags[0])

        cache_merge = []
        seen = set()
        for item in keywords_list:
            if item not in seen:
                cache_merge.append(item)
                seen.add(item)
        # get_rebuild = self.request.get('get_rebuild')


        save_cache.save_cache = cache_merge
        save_cache.put()
        print 'save ---- save ------'
        self.redirect('/createpage')