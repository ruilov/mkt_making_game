import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb

def key():
  return ndb.Key("myEntity","myKey")

class Count(ndb.Model):
  count = ndb.IntegerProperty()

class Quizzes(webapp2.RequestHandler):
  def get(self):
    jsonStr = simplejson.dumps({
      "quizzes": ["week1","week2"]
    })

    self.response.out.write(jsonStr)