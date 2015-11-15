import webapp2,urllib,os,jinja2,utils
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import mail
from quiz_model import Quiz
from user_model import getUser

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class Sendmail(webapp2.RequestHandler):  
  def post(self):
    user = getUser(self)
    if not user or not user.is_admin():
      utils.write_back(self,{"not_allowed": 1})
      return

    user_emails = []
    user_names = []
    if(len(user_emails)>400):
        utils.write_back(self,{"too many users": 1})
        return

    # get the active quiz
    query = Quiz.query().fetch()
    the_quiz = None
    for quiz in query:
      if quiz.status != "active": continue
      if the_quiz != None: 
        utils.write_back(self,{"too many active quizzes": 1})
        return
      the_quiz = quiz
    
    if the_quiz == None:
      utils.write_back(self,{"no active quiz": 1})
      return

    json = simplejson.loads(self.request.body)
    is_test = json["test"]
    is_test = True  # only testing version allowed for now
    if is_test:
      user_emails = [utils.get_user_email(self)]
      user_names = [urllib.quote(utils.get_user_email(self))]

    template = JINJA_ENVIRONMENT.get_template("html/email.html")
    message = mail.EmailMessage()
    message.sender = "mktmakinggame@gmail.com"
    message.subject = "The Market Making Game - new quiz available"

    for i in range(0,len(user_emails)):
      template_values = {
        "user": user_names[i],
        "user_hash": utils.unsubscribeHash(user_names[i]),
        "quiz_url": the_quiz.url(),
        "num_questions": len(the_quiz.questions)
      }
      message.html = template.render(template_values)
      message.to = user_emails[i]
      message.to = "ruilov@gmail.com"
      message.send()

    utils.write_back(self,{"successful": 1})
