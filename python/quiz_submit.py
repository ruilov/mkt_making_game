import webapp2,lookup_util,utils
from django.utils import simplejson
from quiz_model import getQuiz
from user_model import Fillout,fillout_key,getUser

class QuizSubmit(webapp2.RequestHandler):  
  def post(self):
    user = getUser(self)
    if not user:
      utils.write_back(self,{"not_allowed": 1})
      return

    json = simplejson.loads(self.request.body)
    quiz_id = json["id"]

    # if the user has already filled this out, don't allow refilling
    # there's no way to make this happen through the UI, but a direct API call could do this
    fillout_query = Fillout.query(Fillout.user_email == user.email,Fillout.quiz_id == quiz_id).fetch()
    if len(fillout_query)>0: return

    quiz = getQuiz(quiz_id)
    fillout = Fillout(parent=fillout_key(user.email,quiz_id),user_email=user.email,quiz_id=quiz_id)
    lows = []
    highs = []
    for i in range(0,len(quiz.questions)):
      guess_low = json['questions'][i]['guess_low']
      guess_high = json['questions'][i]['guess_high']
      lows.append(float(guess_low))
      highs.append(float(guess_high))

    fillout.guesses_low = lows
    fillout.guesses_high = highs 
    fillout.ranked = (quiz.status == "active")
    fillout.put()

    ans = lookup_util.do_lookup(self)
    utils.write_back(self,ans)