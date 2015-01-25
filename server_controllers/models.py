import webapp2,datetime
from google.appengine.ext import ndb
from server_controllers import utils

class Question(ndb.Model):
  text = ndb.TextProperty()
  source = ndb.TextProperty()
  answer = ndb.TextProperty()

def quiz_key(quiz_id):
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
  query = Quiz.query(ancestor=quiz_key(quiz_id))
  response = query.fetch(1)
  if(len(response)==0):
    quiz = Quiz(parent=quiz_key(quiz_id))
    quiz.status = "editor"
    quiz.questions = [Question()]
  else:
    quiz = response[0]
  return quiz

class User(ndb.Model):
  email = ndb.TextProperty(indexed=True)
  name = ndb.TextProperty()
  subscribed = ndb.BooleanProperty()

class Fillout(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  user_email = ndb.TextProperty(indexed=True)
  guesses_low = ndb.FloatProperty(repeated=True)
  guesses_high = ndb.FloatProperty(repeated=True)
  ranked = ndb.BooleanProperty()

class QuestionRatings(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  user_email = ndb.TextProperty(indexed=True)
  ratings = ndb.IntegerProperty(repeated=True)

class Suggestion(ndb.Model):
  user_email = ndb.TextProperty(indexed=True)
  text = ndb.TextProperty()
  time = ndb.DateTimeProperty()

def check_user_in_db(request):
  user_name = utils.get_user_name(request)
  user_email = utils.get_user_email(request)
  if not user_name or not user_email:
    raise Exception("creating empty user!")

  query = User.query(User.email==user_email).fetch()
  if(len(query)==0):
    ndb_user = User(email=user_email,name=user_name,subscribed=True)
    ndb_user.put()
  elif utils.get_user_provider(request)=="facebook":
    old_user = query[0]
    if old_user.name != utils.get_user_name(request):
      old_user.name = utils.get_user_name(request)
      old_user.put()
