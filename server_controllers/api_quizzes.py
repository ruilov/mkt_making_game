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

    utils.write_back(self,{"quizzes": quizzes})

  def post(self,qs):
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
      score_quiz(quiz,quiz_id)
      quiz.status = "old"
      quiz.put()


def score_quiz(quiz,quiz_id):
  user_ids = []
  points = []

  user_query = models.User.query()
  user_results = user_query.fetch()
  for user in user_results:
    fillout_query = models.Fillout.query(models.Fillout.user_id == user.user_id, models.Fillout.quiz_id == quiz_id)
    fillout_res = fillout_query.fetch(1)
    if len(fillout_res)==0: continue
    
    point = 0
    fillout = fillout_res[0]
    for i in range(0,len(quiz.questions)):
      ans = float(quiz.questions[i].answer)
      low = float(fillout.guesses_low[i])
      high = float(fillout.guesses_high[i])
      if low <= ans and ans <= high:
        point+=1

    user_ids.append(user.user_id)
    points.append(point)

  # now that we calculated the rankings, save them to the DB
  rank_query = models.QuizRanking.query(ancestor=models.quiz_ranking_key(quiz_id))
  rank_res = rank_query.fetch(1)
  if(len(rank_res)==0):
    ranking = models.QuizRanking(parent=models.quiz_ranking_key(quiz_id),quiz_id=quiz_id)
  else: 
    ranking = rank_res[0]
  ranking.user_ids = user_ids
  ranking.points = points
  ranking.put()
