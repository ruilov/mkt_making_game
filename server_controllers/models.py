import webapp2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

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

  def hasFilled(self):
    user = users.get_current_user()
    if not user: return False
    fillout_query = Fillout.query(Fillout.user_id == user.user_id(), Fillout.quiz_id == self.getID())
    return len(fillout_query.fetch()) > 0

def user_key(user_id):
  return ndb.Key("User",str(user_id))

class User(ndb.Model):
  user_id = ndb.TextProperty()
  email = ndb.TextProperty()
  nickname = ndb.TextProperty()
  subscribed = ndb.BooleanProperty()

class Fillout(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  user_id = ndb.TextProperty(indexed=True)
  guesses_low = ndb.FloatProperty(repeated=True)
  guesses_high = ndb.FloatProperty(repeated=True)

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

def check_user_in_db(user):
  user_id = user.user_id()
  query = User.query(ancestor=user_key(user_id))
  response = query.fetch(1)
  if(len(response)==0):
    ndb_user = User(parent=user_key(user_id))
    ndb_user.user_id = user_id
    ndb_user.email = user.email()
    ndb_user.nickname = user.nickname()
    ndb_user.subscribed = True
    ndb_user.put()