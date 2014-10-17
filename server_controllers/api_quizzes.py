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

    if "editor" in status and not utils.is_admin():
      utils.write_back(self,{"not_allowed": 1})
      return

    query = models.Quiz.query().fetch()
    quizzes = []
    for quiz in query:
      if quiz.status not in status: continue;
      quiz_dict = quiz.to_dict();
      quiz_dict["id"] = quiz.key.parent().id()
      quizzes.append(quiz_dict)

    utils.write_back(self,{"quizzes": quizzes})

  def post(self,qs):
    if not utils.is_admin():
      utils.write_back(self,{"not_allowed": 1})
      return

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
  points_by_uid = {}
  points = []

  fillout_query = models.Fillout.query(models.Fillout.quiz_id == quiz_id).fetch()
  for fillout in fillout_query:
    point = 0
    for i in range(0,len(quiz.questions)):
      ans = float(quiz.questions[i].answer)
      low = float(fillout.guesses_low[i])
      high = float(fillout.guesses_high[i])
      if low <= ans and ans <= high:
        point+=1

    points_by_uid[fillout.user_id]=point

  # now that we calculated the rankings, save them to the DB
  rank_query = models.QuizRanking.query(ancestor=models.quiz_ranking_key(quiz_id))
  rank_res = rank_query.fetch(1)
  if(len(rank_res)==0):
    ranking = models.QuizRanking(parent=models.quiz_ranking_key(quiz_id),quiz_id=quiz_id)
  else: 
    ranking = rank_res[0]
  ranking.user_ids = points_by_uid.keys()
  ranking.points = points_by_uid.values()
  ranking.put()
