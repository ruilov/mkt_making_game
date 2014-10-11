import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class Quizzes(webapp2.RequestHandler):
  def get(self,qs):
    status = self.request.get("status")

    query = models.Quiz.query()
    response = query.fetch()
    quizzes = []
    for quiz in response:
      if quiz.status not in status: continue;
      quiz_dict = quiz.to_dict();
      quiz_dict["id"] = quiz.key.parent().id()
      quizzes.append(quiz_dict)

    jsonStr = simplejson.dumps({"quizzes": quizzes}, cls = utils.MyEncoder)
    self.response.out.write(jsonStr)

  def post(self,qs):
    json = simplejson.loads(self.request.body)
    if json["action"] == "delete":
      key = models.getQuiz(json["id"]).key
      key.delete()
    elif json["action"] == "activate":
      quiz = models.getQuiz(json["id"])
      quiz.status = "active"
      quiz.put()
    elif json["action"] == "deactivate":
      quiz = models.getQuiz(json["id"])
      quiz.status = "editor"
      quiz.put()