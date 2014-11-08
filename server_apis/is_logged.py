import webapp2
from server_controllers import utils

class IsLogged(webapp2.RequestHandler):
  def get(self):
    ans = {"logged": False}
    if utils.get_user_name(self):
      ans["logged"] = True
    utils.write_back(self,ans)
