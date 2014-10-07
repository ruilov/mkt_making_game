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

def user_key(user_id):
  return ndb.key("User",str(user_id))

class User(ndb.Model):
  user_id = ndb.TextProperty()
  email = ndb.TextProperty()
  nickname = ndb.TextProperty()

class Fillout(ndb.Model):
  quiz_id = ndb.IntegerProperty()
  user_id = ndb.TextProperty()
  guesses_low = ndb.IntegerProperty(repeated=True)
  guesses_high = ndb.IntegerProperty(repeated=True)
