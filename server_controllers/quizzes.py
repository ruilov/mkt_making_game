import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb

def key():
  return ndb.Key("myEntity","myKey")

class Count(ndb.Model):
  count = ndb.IntegerProperty()

class Quizzes(webapp2.RequestHandler):
  def get(self):
    jsonStr = simplejson.dumps({
      "quizzes": [
        {"name": "week1", "time": str(datetime.datetime.now())},
        {"name": "week2", "time": str(datetime.datetime.now())},
        {"name": "week3", "time": str(datetime.datetime.now())},
        {"name": "week4", "time": str(datetime.datetime.now())},
        {"name": "week5", "time": str(datetime.datetime.now())},
      ]
    })

    self.response.out.write(jsonStr)