import webapp2
from django.utils import simplejson

from server_controllers import models,utils

# REST api for retrieving scores so that we can play with the methodology

class Scores(webapp2.RequestHandler):
  def get(self,idStr):
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    quiz_dict = quiz.to_dict()

    user_query = models.User.query().fetch()
    
    answer = {"questions": []}
    for question in quiz.questions:
      q = question.to_dict()
      q["guesses"] = {}
      answer["questions"].append(q)

    for user in user_query:
      fillout_query = models.Fillout.query(models.Fillout.user_email == user.email, models.Fillout.quiz_id == quiz_id)
      fillout_res = fillout_query.fetch(1)
      if len(fillout_res)==0: continue
      
      fillout = fillout_res[0]
      for i in range(0,len(answer["questions"])):
        answer["questions"][i]["guesses"][user.email] = {
          "low": fillout.guesses_low[i],
          "high": fillout.guesses_high[i],
        }

    utils.write_back(self,answer)
