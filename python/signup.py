import webapp2,lookup_util,utils
from django.utils import simplejson
from google.appengine.ext import ndb
from user_model import User,cookieHash

class SignUp(webapp2.RequestHandler):
  def post(self):
    json = simplejson.loads(self.request.body)
    all_users = User.query().fetch()

    nextID = -1
    for user in all_users:
      if user.email == json["email"]:
        utils.write_back(self,{"email exists": 1})
        return

      if user.name == json["username"]:
        utils.write_back(self,{"username exists": 1})
        return

      nextID = max(nextID,user.unique_id+1)

    new_user = User(unique_id=nextID,email=json["email"],name=json["username"],subscribed=True)
    new_user.password = new_user.password_hash(json["password"])
    new_user.put()

    self.response.set_cookie('id', urllib.quote(str(new_user.unique_id)))
    self.response.set_cookie('hash', urllib.quote(cookieHash(new_user.unique_id)))

    ans = lookup_util.do_lookup(self,new_user)
    utils.write_back(self,ans)