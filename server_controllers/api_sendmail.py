import webapp2
from string import Template
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
    user_names = []
    if(len(user_emails)>400):
        utils.write_back(self,{"too_many_users": 1})
        return

    json = simplejson.loads(self.request.body)
    is_test = json["test"]
    is_test = True  # only testing version allowed for now
    if is_test:
      user = users.get_current_user()
      user_emails = [user.email()]
      user_names = [user.user_id()]

    message = mail.EmailMessage()
    message.sender = "mktmakinggame.com <mktmakinggame@gmail.com>"
    message.subject = "New quiz available at mktmakinggame.com"
    html_template = Template("""\
        <html>
          <head></head>
          <body>
            There's a new quiz available at <a href="http://mktmakinggame.com">mktmakinggame.com</a>. Have fun!
            <br><br>
            And remember: <b>no cheating allowed</b>, please don't do any internet searches while answering the quiz.
            <br><br>
            Unsubscribe <a href="http://mktmakinggame.com/unsubscribe/?user=$user&hashtag=$hashtag">here</a>
          </body>
        </html>
        """)

    for i in range(0,len(user_emails)):
      message.html = html_template.substitute(user=user_names[i], hashtag=utils.unsubscribeHash(user_names[i]))
      message.to = user_emails[i]
      # print message.html
      message.send()

    utils.write_back(self,{"successful": 1})
