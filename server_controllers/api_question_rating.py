import webapp2
from django.utils import simplejson
from google.appengine.api import users
from server_controllers import models

class QuestionRating(webapp2.RequestHandler):
  def post(self,idStr):
    ''' called whenever the user rates a question'''
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    json = simplejson.loads(self.request.body)

    question = json['question']
    rat = json['rating']
    
    user = users.get_current_user()
    user_id = user.user_id()
    query = models.QuestionRatings.query(models.QuestionRatings.user_id == user_id, models.QuestionRatings.quiz_id == quiz_id).fetch()
    if len(query)==0:
      rating = models.QuestionRatings(user_id=user_id,quiz_id=quiz_id,ratings=[])
      for i in range(0,len(quiz.questions)):
        rating.ratings.append(-1)
    else:
      rating = query[0]

    rating.ratings[question] = rat
    rating.put()