import webapp2
from server_controllers import utils
import lookup_util

class Lookup(webapp2.RequestHandler):
  def get(self):
    ans = lookup_util.do_lookup(self)
    utils.write_back(self,ans)

