import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb

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

def user_key(user_id):
  return ndb.Key("User",str(user_id))

class User(ndb.Model):
  user_id = ndb.TextProperty()
  email = ndb.TextProperty()
  nickname = ndb.TextProperty()

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
    quiz.questions = [Question()]
  else:
    quiz = response[0]

  return quiz