import webapp2, urllib, lookup_util, utils
from django.utils import simplejson
from google.appengine.ext import ndb
from user_model import User,cookieHash

class SignIn(webapp2.RequestHandler):
  def post(self):
    json = simplejson.loads(self.request.body)
    username = json["username"]

    all_users = User.query().fetch()

    for user in all_users:
      if user.name != json["username"] and user.email != json["username"]:
        continue
        
      if not user.checkPassword(json["password"]):
        utils.write_back(self,{"incorrect": 1})
        return

      self.response.set_cookie('username', urllib.quote(user.name))
      self.response.set_cookie('hash', urllib.quote(cookieHash(user.name)))
      
      ans = lookup_util.do_lookup(self,user)
      utils.write_back(self,ans)
      return

    utils.write_back(self,{"incorrect": 1})
    