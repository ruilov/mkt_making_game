import webapp2,lookup_util,utils,urllib
from django.utils import simplejson
from google.appengine.ext import ndb
from user_model import User,cookieHash

class SignUp(webapp2.RequestHandler):
  def post(self):
    json = simplejson.loads(self.request.body)
    all_users = User.query().fetch()

    hashs = json["resetHash"]
    email = json["email"]
    username = json["username"]
    password = json["password"]

    user = None
    if len(hashs)>0:
      if not utils.checkResetHash(email,hashs):
        utils.write_back(self,{"invalid hash": 1})
        return

      users = User.query().fetch()
      for ui in users:
        if ui.email == email:
          user = ui
          break
        
      if user == None:
        utils.write_back(self,{"invalid hash": 1})
        return

    else:
      nextID = -1
      for user in all_users:
        if user.email == email:
          utils.write_back(self,{"email exists": 1})
          return

        if user.name == username:
          utils.write_back(self,{"username exists": 1})
          return

        nextID = max(nextID,user.unique_id+1)

      user = User(unique_id=nextID,email=email,name=username,subscribed=True)

    user.password = user.password_hash(password)
    user.put()

    self.response.set_cookie('id', urllib.quote(str(user.unique_id)))
    self.response.set_cookie('hash', urllib.quote(cookieHash(user.unique_id)))

    ans = lookup_util.do_lookup(self,user)
    utils.write_back(self,ans)