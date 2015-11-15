from google.appengine.ext import ndb
import utils
from user_model import Fillout

class Question(ndb.Model):
  text = ndb.TextProperty()
  source = ndb.TextProperty()
  answer = ndb.TextProperty()

def __quiz_key(quiz_id):
  return ndb.Key("Quiz",str(quiz_id))

class Quiz(ndb.Model):
  questions = ndb.StructuredProperty(Question,repeated=True)
  status = ndb.TextProperty()
  releaseDate = ndb.DateTimeProperty()

  def getID(self):
    return self.key.parent().id()

  def url(self,full=True):
    url = "/#/quiz?id="+self.getID();
    if full: url = "http://mktmakinggame.com" + url
    return url

  def hasFilled(self,request):
    user_email = utils.get_user_email(request)
    if not user_email: return False
    fillout_query = Fillout.query(Fillout.user_email == user_email, Fillout.quiz_id == self.getID())
    return len(fillout_query.fetch()) > 0

def getQuiz(quiz_id):
  query = Quiz.query(ancestor=__quiz_key(quiz_id))
  response = query.fetch(1)
  if(len(response)==0):
    quiz = Quiz(parent=__quiz_key(quiz_id))
    quiz.status = "editor"
    quiz.questions = []
  else:
    quiz = response[0]
  return quiz
