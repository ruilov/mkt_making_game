import webapp2
from django.utils import simplejson
from server_controllers import utils
from models.user_model import QuestionRatings
from models.quiz_model import getQuiz

class RateQuestion(webapp2.RequestHandler):
  def post(self):
    if not utils.is_logged(self):
      utils.write_back(self,{"not_allowed": 1})
      return
    
    json = simplejson.loads(self.request.body)  
    quiz_id = json["quiz_id"]
    quiz = getQuiz(quiz_id)
    
    user_email = utils.get_user_email(self)
    query = QuestionRatings.query(QuestionRatings.user_email==user_email,QuestionRatings.quiz_id==quiz_id).fetch()
    if len(query)==0:
      rating = QuestionRatings(user_email=user_email,quiz_id=quiz_id,ratings=[])
      for i in range(0,len(quiz.questions)):
        rating.ratings.append(-1)
    else:
      rating = query[0]

    rating.ratings[json["qIdx"]] = json["rating"]
    rating.put()