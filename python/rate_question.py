import webapp2,utils
from django.utils import simplejson
from user_model import QuestionRatings,getUser
from quiz_model import getQuiz

class RateQuestion(webapp2.RequestHandler):
  def post(self):
    user = getUser(self)
    if not user:
      utils.write_back(self,{"not_allowed": 1})
      return

    json = simplejson.loads(self.request.body)  
    quiz_id = json["quiz_id"]
    quiz = getQuiz(quiz_id)
    
    query = QuestionRatings.query(QuestionRatings.username==user.name,QuestionRatings.quiz_id==quiz_id).fetch()
    if len(query)==0:
      rating = QuestionRatings(username=user.name,quiz_id=quiz_id,ratings=[])
      for i in range(0,len(quiz.questions)):
        rating.ratings.append(-1)
    else:
      rating = query[0]

    rating.ratings[json["qIdx"]] = json["rating"]
    rating.put()