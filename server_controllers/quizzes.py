import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,quiz_editor

class Quizzes(webapp2.RequestHandler):
  def get(self,qs):
    include_released = self.request.get("released")
    include_unreleased = self.request.get("unreleased")

    query = models.Quiz.query()
    response = query.fetch()
    quizzes = []
    for quiz in response:

      if quiz.released and ( not include_released ): continue;
      if ( not quiz.released ) and ( not include_unreleased ): continue;

      id = quiz.key.parent().id()
      elem = {"id": id}
      if quiz.releaseDate: elem["releaseDate"] = quiz.releaseDate.isoformat()
      quizzes.append(elem)

    jsonStr = simplejson.dumps({"quizzes": quizzes})
    self.response.out.write(jsonStr)

  def post(self):
    id = self.request.body
    key = quiz_editor.getQuiz(id).key
    key.delete()