import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users

from server_controllers import models,quiz_editor

class QuizFillout(webapp2.RequestHandler):
  def post(self,idStr):
    quiz_id = self.request.get("id")
    quiz = quiz_editor.getQuiz(quiz_id)
    
    json = simplejson.loads(self.request.body)

    user = users.get_current_user()
    user_id = user.user_id()

    fillout = models.Fillout(user_id=user_id,quiz_id=int(quiz_id))
    lows = []
    highs = []
    for i in range(0,len(quiz.questions)):
      guess_low = json['questions'][i]['guess_low']
      guess_high = json['questions'][i]['guess_high']
      lows.append(int(guess_low))
      highs.append(int(guess_high))

    fillout.guesses_low = lows
    fillout.guesses_high = highs 

    print(fillout)