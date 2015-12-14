
import os
import urllib
import time
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import images
from webapp2_extras import sessions
from recipe import User

import jinja2
import webapp2

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('template/main_page.html')
        self.response.write(template.render())

class LoginPage(BaseHandler):
    def post(self):
        user_name = self.request.get('user_name')
        user_id = self.request.get('user_id')
        user_friends = json.loads(self.request.get('user_friends'))
        photo = self.request.get('photo')
        print photo
        self.session['user_name'] = user_name
        self.session['user_id'] = user_id
        user = User.get_by_id(user_id)
        if not user:
            user = User(id=user_id)
            user.user_id = user_id
            user.user_name = user_name
            user.friends = [friend['id'] for friend in user_friends]
            user.photo = photo
            user.put()
            time.sleep(1)
        else:
            user.friends = [friend['id'] for friend in user_friends]
            user.photo = photo
            user.put()
            time.sleep(1)
        self.redirect('/createpage')