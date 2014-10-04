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
        {"id": 1, "name": "week1", "time": str(datetime.datetime.now())},
        {"id": 2, "name": "week2", "time": str(datetime.datetime.now())},
        {"id": 3, "name": "week3", "time": str(datetime.datetime.now())},
        {"id": 4, "name": "week4", "time": str(datetime.datetime.now())},
        {"id": 5, "name": "week5", "time": str(datetime.datetime.now())},
      ]
    })

    self.response.out.write(jsonStr)