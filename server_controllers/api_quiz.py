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
    if len(quiz_id)==0:
      utils.write_back(self,{"no_quiz_id": 1})
      return

    quiz = models.getQuiz(quiz_id)

    # check if the user is allowed to see this quiz
    if quiz.status=="editor" and not utils.is_admin():
      utils.write_back(self,{"not_allowed": 1})
      return

    quiz_dict = quiz.to_dict()
    quiz_dict["state"] = "display_only"

    # find a fillout for this quiz
    user = users.get_current_user()
    if user:
      models.check_user_in_db(user)
      user_id = user.user_id()

      fillout_query = models.Fillout.query(models.Fillout.user_id == user_id, models.Fillout.quiz_id == quiz_id)
      fillout_res = fillout_query.fetch(1)
      if len(fillout_res)!=0:
        fillout_quiz(quiz_dict,fillout_res[0])

    # remove the answers from active quizzes if the user hasn't filled them out
    if quiz_dict["state"] != "filled" and quiz_dict["status"]=="active":
      quiz_dict["state"] = "to_fill"
      for question in quiz_dict["questions"]: del question["answer"]

    utils.write_back(self,quiz_dict)
  
  def post(self,idStr):
    ''' this will be called when the user fills out a quiz. It will create a Fillout entity in the database
    and then write back the quiz, with the fillout data, so that the new html page can be rendered to the user'''

    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)

    # if this is not an active quiz then don't allow fill outs for it
    if quiz.status!="active":
      utils.write_back(self,{"not_active": 1})
      return

    # fixme: if the user already filled it out then don't allow it again

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
    utils.write_back(self,quiz_dict)

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
  quiz_dict["state"]="filled"