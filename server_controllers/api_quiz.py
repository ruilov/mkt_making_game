import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users

from server_controllers import models,utils

class Quiz(webapp2.RequestHandler):
  def get(self,idStr):
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    quiz_dict = quiz.to_dict()

    # find a fillout for this quiz
    user = users.get_current_user()
    if user:
      user_id = user.user_id()
      query = models.User.query(ancestor=models.user_key(user_id))
      response = query.fetch(1)
      if len(response)!=0:
        fillout_query = models.Fillout.query(models.Fillout.user_id == user_id, models.Fillout.quiz_id == quiz_id)
        fillout_res = fillout_query.fetch(1)
        if len(fillout_res)!=0:
          fillout_quiz(quiz_dict,fillout_res[0])

    jsonStr = simplejson.dumps(quiz_dict, cls = utils.MyEncoder)
    self.response.out.write(jsonStr)

  def post(self,idStr):
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    json = simplejson.loads(self.request.body)
    user = users.get_current_user()
    user_id = user.user_id()
    fillout = models.Fillout(user_id=user_id,quiz_id=quiz_id)
    lows = []
    highs = []
    for i in range(0,len(quiz.questions)):
      guess_low = json['questions'][i]['guess_low']
      guess_high = json['questions'][i]['guess_high']
      lows.append(float(guess_low))
      highs.append(float(guess_high))

    fillout.guesses_low = lows
    fillout.guesses_high = highs 
    fillout.put()

    # construct the response to send back to display to the user
    quiz_dict = quiz.to_dict()
    fillout_quiz(quiz_dict,fillout)
    jsonStr = simplejson.dumps(quiz_dict, cls = utils.MyEncoder)
    self.response.out.write(jsonStr)

def fillout_quiz(quiz_dict,fillout):
  for i in range(0,len(quiz_dict["questions"])):
    quiz_dict["questions"][i]["guess_low"] = fillout.guesses_low[i]
    quiz_dict["questions"][i]["guess_high"] = fillout.guesses_high[i]

    ans = float(quiz_dict["questions"][i]["answer"])
    low = float(fillout.guesses_low[i])
    high = float(fillout.guesses_high[i])

    if(ans<low):
      quiz_dict["questions"][i]["status"] = "Hit bid"
    elif(ans>high):
      quiz_dict["questions"][i]["status"] = "Lift offer"
    else:
      quiz_dict["questions"][i]["status"] = "No trade"
  quiz_dict["has_fillout"]=True