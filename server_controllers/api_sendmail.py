import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users

from server_controllers import utils
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from google.appengine.api import mail

class SendMail(webapp2.RequestHandler):  
  def post(self):
    if not utils.is_admin(): 
      utils.write_back(self,{"not_allowed": 1})
      return

    user_emails = []
    if(len(user_emails)>400):
        utils.write_back(self,{"too_many_users": 1})
        return

    json = simplejson.loads(self.request.body)
    is_test = json["test"]
    is_test = True  # only testing version allowed for now
    if is_test:
      user = users.get_current_user()
      user_emails = [user.email()]

    message = mail.EmailMessage()
    message.sender = "mktmakinggame.com <mktmakinggame@gmail.com>"
    message.subject = "New quiz available at mktmakinggame.com"
    message.html = """\
      <html>
        <head></head>
        <body>
          There's a new quiz available at <a href="http://mktmakinggame.com">mktmakinggame.com</a>. Have fun!
          <br><br>
          And remember: <b>no cheating allowed</b>, please don't do any internet searchs while answering the quiz.
        </body>
      </html>
      """
    message.to = user_emails[0]
    message.send()
    utils.write_back(self,{"successful": 1})
