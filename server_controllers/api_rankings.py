import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class Rankings(webapp2.RequestHandler):
  def get(self,qs):
    rank_query = models.QuizRanking.query()
    rank_res = rank_query.fetch()

    rank_by_user = {}
    quiz_dates = []
    user_id_map = {}

    for ranking in rank_res:
      # get info about the quiz
      quiz_id = ranking.quiz_id
      quiz = models.getQuiz(quiz_id)
      quiz_dates.append({"quiz_id": quiz_id, "releaseDate": quiz.releaseDate})

      for i in range(0,len(ranking.user_ids)):
        # check that we already know the nickname of this user
        user_id = ranking.user_ids[i]        
        if user_id not in user_id_map:
          user_query = models.User.query(ancestor=models.user_key(user_id))
          user_res = user_query.fetch(1)
          if len(user_res)==0: continue
          user_id_map[user_id]=user_res[0].nickname

        user = user_id_map[user_id]
        if user not in rank_by_user:
          rank_by_user[user] = {}

        rank_by_user[user][quiz_id] = ranking.points[i]

    # sort the quizzes by date
    quiz_dates.sort(key=lambda elem: elem["releaseDate"])
    
    utils.write_back(self,{"rank_by_user": rank_by_user, "quiz_dates": quiz_dates})