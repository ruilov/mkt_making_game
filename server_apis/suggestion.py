import webapp2, datetime
from django.utils import simplejson
from server_controllers import models,utils
from google.appengine.api import mail

class Suggestion(webapp2.RequestHandler):  
  def post(self):
    # get the data
    json = simplejson.loads(self.request.body)
    suggestion = json["suggestion"]
    user_email = utils.get_user_email(self)

    # save to the db
    sModel = models.Suggestion(user_email=user_email,text=suggestion,time=datetime.datetime.now())
    sModel.put()

    # send a notification
    message = mail.EmailMessage()
    message.sender = "mktmakinggame.com <mktmakinggame@gmail.com>"
    message.subject = "New suggestion from " + user_email
    message.html = suggestion
    message.to = "mktmakinggame@gmail.com"
    message.send()