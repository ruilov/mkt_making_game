import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,quiz_editor

class Quizzes(webapp2.RequestHandler):
  def get(self):
    query = models.Quiz.query()
    response = query.fetch()
    quizzes = []
    for quiz in response:
      id = quiz.key.parent().id()
      quizzes.append({
        "id": id,
      })

    jsonStr = simplejson.dumps({"quizzes": quizzes})
    self.response.out.write(jsonStr)

  def post(self):
    id = self.request.body
    key = quiz_editor.getQuiz(id).key
    key.delete()