import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users

from server_controllers import models,utils

# this class is the API for getting the questions of a quiz to display to the user and
# for the user to fill out a quiz. It will also show questions of the quiz even after
# the user filled it out

class Quiz(webapp2.RequestHandler):
  def get(self,idStr):
    '''returns the questions of a quiz to be shown to the user. If the user has already filled out this
    quiz, then find the Fillout entity and scope the quiz'''
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
    ''' this will be called when the user fills out a quiz. It will create a Fillout entity in the database
    and then write back the quiz, with the fillout data, so that the new html page can be rendered to the user'''

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
  '''populates the quiz_dict with the guesses from the fillout and whether they were correct'''

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