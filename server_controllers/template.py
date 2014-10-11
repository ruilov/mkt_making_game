import webapp2
import os
import jinja2
from google.appengine.api import users
from server_controllers import models,utils

# this is the controller for all HTML pages

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class TemplatePage(webapp2.RequestHandler):
  def get(self,path):
    template_path = "template.html"
    template_values = {
      "user_login_url": users.create_login_url('/'),
      "is_admin": utils.is_admin(),
    }

    if(path!=""): template_path = path

    user = users.get_current_user()
    if user:
      template_values["usernick"] = user.nickname()
      template_values["user_logout_url"] = users.create_logout_url('/')
      if template_path == "template.html":
        check_user_in_db(user)

    template = JINJA_ENVIRONMENT.get_template("html/"+template_path)
    self.response.write(template.render(template_values))

def check_user_in_db(user):
  user_id = user.user_id()
  query = models.User.query(ancestor=models.user_key(user_id))
  response = query.fetch(1)
  if(len(response)==0):
    ndb_user = models.User(parent=models.user_key(user_id))
    ndb_user.user_id = user_id
    ndb_user.email = user.email()
    ndb_user.nickname = user.nickname()
    ndb_user.put()
