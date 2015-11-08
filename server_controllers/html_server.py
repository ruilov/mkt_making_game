import webapp2,os,jinja2
import utils

# this is the controller for all HTML pages

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class HTMLServer(webapp2.RequestHandler):
  def get(self,path):
    resolved_path = "template.html"
    if(path!=""): resolved_path = path

    template_values = {
      "gmail_login_url": utils.get_login_url("gmail"),
      "facebook_login_url": utils.get_login_url("facebook"),
      "is_admin": utils.is_admin(self),
    }

    # TODO: permissioning here is a weird thing
    allowed_not_logged = ["template.html","loading.html","login.html","not_allowed.html"]
    if not utils.is_logged(self) and resolved_path not in allowed_not_logged:
      resolved_path="login.html"

    user_name = utils.get_user_name(self)
    if user_name:
      template_values["user_name"] = user_name
      template_values["logout_url"] = utils.get_logout_url()

    template = JINJA_ENVIRONMENT.get_template("html/"+resolved_path)
    self.response.write(template.render(template_values))

