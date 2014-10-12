import webapp2
from server_controllers import utils
from google.appengine.api import users

class IsLogged(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    ans = {"logged": False}
    if user: ans["logged"]=True
    utils.write_back(self,ans)
