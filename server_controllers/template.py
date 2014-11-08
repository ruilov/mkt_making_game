import webapp2,os,jinja2
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
      "gmail_login_url": utils.get_login_url("gmail"),
      "facebook_login_url": utils.get_login_url("facebook"),
      "is_admin": utils.is_admin(self),
    }

    if(path!=""): template_path = path

    allowed_not_logged = ["template.html","index.html","login.html","not_allowed.html"]
    if not utils.is_logged(self) and template_path not in allowed_not_logged:
      template_path="login.html"

    user_name = utils.get_user_name(self)
    if user_name:
      template_values["user_name"] = user_name
      template_values["logout_url"] = utils.get_logout_url()

    template = JINJA_ENVIRONMENT.get_template("html/"+template_path)
    self.response.write(template.render(template_values))

