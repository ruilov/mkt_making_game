import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

class Quizzes(webapp2.RequestHandler):
  def get(self,qs):
    status = self.request.get("status")

    query = models.Quiz.query()
    response = query.fetch()
    quizzes = []
    for quiz in response:
      if quiz.status != status: continue;
      id = quiz.key.parent().id()
      elem = {"id": id}
      if quiz.releaseDate: elem["releaseDate"] = quiz.releaseDate
      quizzes.append(elem)

    jsonStr = simplejson.dumps({"quizzes": quizzes}, cls = utils.MyEncoder)
    self.response.out.write(jsonStr)

  def post(self,qs):
    id = self.request.body
    key = models.getQuiz(id).key
    key.delete()