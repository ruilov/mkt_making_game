import webapp2,urllib
from string import Template
from django.utils import simplejson
from google.appengine.ext import ndb
import webapp2,os,jinja2
from server_controllers import utils
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class SendMail(webapp2.RequestHandler):  
  def post(self):
    if not utils.is_admin(self): 
      utils.write_back(self,{"not_allowed": 1})
      return

    user_emails = []
    user_names = []
    if(len(user_emails)>400):
        utils.write_back(self,{"too_many_users": 1})
        return

    json = simplejson.loads(self.request.body)
    is_test = json["test"]
    is_test = True  # only testing version allowed for now
    if is_test:
      user_emails = [utils.get_user_email(self)]
      user_names = [urllib.quote(utils.get_user_email(self))]

    template = JINJA_ENVIRONMENT.get_template("html/email.html")
    message = mail.EmailMessage()
    message.sender = "mktmakinggame.com <mktmakinggame@gmail.com>"
    message.subject = "New Quiz at The Market Making Game"

    for i in range(0,len(user_emails)):
      template_values = {
        "user": user_names[i],
        "user_hash": utils.unsubscribeHash(user_names[i]),
        "domain": "mktmakinggame.com"
      }
      message.html = template.render(template_values)
      message.to = user_emails[i]
      message.send()

    utils.write_back(self,{"successful": 1})
