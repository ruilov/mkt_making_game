import webapp2, urllib, jinja2, lookup_util, utils
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import mail
from user_model import User,cookieHash

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class Reset(webapp2.RequestHandler):
  def get(self,qs):
    email = urllib.unquote(self.request.get("email"))
    hashs = self.request.get("hash")

    if not utils.checkResetHash(email,hashs):
      return

    users = User.query().fetch()
    for user in users:
      if user.email != email: continue
      template = JINJA_ENVIRONMENT.get_template("html/template.html")
      template_values = {}
      self.response.write(template.render(template_values))
      return
    
  def post(self):
    json = simplejson.loads(self.request.body)
    username = json["username"]

    user = None
    users = User.query().fetch()
    for ui in users:
      if ui.email == username or ui.name == username:
        user = ui
        break

    if user:
      template = JINJA_ENVIRONMENT.get_template("html/password_reset.html")
      message = mail.EmailMessage()
      message.sender = "mktmakinggame@gmail.com"
      message.subject = "The Market Making Game - reset your password"

      template_values = {"link": utils.resetLink(user.email,user.name)}
      message.html = template.render(template_values)
      message.to = user.email
      message.send()