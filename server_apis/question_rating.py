import webapp2
from django.utils import simplejson
from server_controllers import models,utils

class QuestionRating(webapp2.RequestHandler):
  def post(self,idStr):
    ''' called whenever the user rates a question'''
    if not utils.is_logged(self):
      utils.write_back(self,{"not_allowed": 1})
      return
      
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    json = simplejson.loads(self.request.body)

    question = json['question']
    rat = json['rating']
    
    user_email = utils.get_user_email(self)
    query = models.QuestionRatings.query(models.QuestionRatings.user_email == user_email, models.QuestionRatings.quiz_id == quiz_id).fetch()
    if len(query)==0:
      rating = models.QuestionRatings(user_email=user_email,quiz_id=quiz_id,ratings=[])
      for i in range(0,len(quiz.questions)):
        rating.ratings.append(-1)
    else:
      rating = query[0]

    rating.ratings[question] = rat
    rating.put()