import webapp2, datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import utils
from models.quiz_model import getQuiz

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class QuizStatusUpdate(webapp2.RequestHandler):
  def post(self,qs):
    if not utils.is_admin(self):
      utils.write_back(self,{"not_allowed": 1})
      return

    json = simplejson.loads(self.request.body)
    quiz = getQuiz(json["id"])
    new_status = json["new_status"]
    if new_status == "delete":
      key = quiz.key
      key.delete()
    else:
      quiz.status = new_status
      if new_status == "active":
        quiz.releaseDate = datetime.datetime.now()
      quiz.put()