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
