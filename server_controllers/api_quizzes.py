import webapp2, datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class Quizzes(webapp2.RequestHandler):
  def get(self,qs):
    if not utils.is_logged(self):
      utils.write_back(self,{"not_allowed": 1})
      return
      
    status = self.request.get("status")

    if "editor" in status and not utils.is_admin(self):
      utils.write_back(self,{"not_allowed": 1})
      return

    query = models.Quiz.query().fetch()
    quizzes = []
    for quiz in query:
      if not( quiz.status in status or (quiz.status=="active" and ("old" in status) and quiz.hasFilled(self))):
        continue
      quiz_dict = quiz.to_dict();
      quiz_dict["id"] = quiz.key.parent().id()
      quizzes.append(quiz_dict)

    utils.write_back(self,{"quizzes": quizzes})

  def post(self,qs):
    if not utils.is_admin(self):
      utils.write_back(self,{"not_allowed": 1})
      return

    json = simplejson.loads(self.request.body)
    if json["action"] == "delete":
      key = models.getQuiz(json["id"]).key
      key.delete()
    elif json["action"] == "activate":
      quiz = models.getQuiz(json["id"])
      quiz.status = "active"
      quiz.releaseDate = datetime.datetime.now()
      quiz.put()
    elif json["action"] == "unold":
      quiz = models.getQuiz(json["id"])
      quiz.status = "editor"
      quiz.put()
    elif json["action"] == "deactivate":
      quiz_id = json["id"]
      quiz = models.getQuiz(quiz_id)
      quiz.status = "old"
      quiz.put()
