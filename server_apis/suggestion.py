import webapp2, datetime
from django.utils import simplejson
from server_controllers import utils
from google.appengine.api import mail
from models.user_model import UserSuggestion

class Suggestion(webapp2.RequestHandler):  
  def post(self):
    json = simplejson.loads(self.request.body)
    if "suggestion" not in json: return

    sug = json["suggestion"]
    user_email = utils.get_user_email(self)

    # save to the db
    sModel = UserSuggestion(user_email = user_email, text = sug, time = datetime.datetime.now())
    sModel.put()

    # send a notification
    message = mail.EmailMessage()
    message.sender = "mktmakinggame@gmail.com"
    message.subject = "New suggestion from " + user_email
    message.html = sug
    message.to = "mktmakinggame@gmail.com"
    message.send()