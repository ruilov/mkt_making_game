import webapp2, datetime,utils
from django.utils import simplejson
from quiz_model import getQuiz
from user_model import getUser

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class QuizStatusUpdate(webapp2.RequestHandler):
  def post(self,qs):
    user = getUser(self)
    if not user or not user.is_admin():
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