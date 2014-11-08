import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users

from server_controllers import models,utils

class Datastore(webapp2.RequestHandler):
  def get(self):

    types = [
      {"tag": "users", "model": models.User},
      {"tag": "quizzes", "model": models.Quiz},
      {"tag": "fillouts", "model": models.Fillout},
      {"tag": "ratings", "model": models.QuestionRatings}
    ]

    datastore = {}
    for t in types:
      datastore[t["tag"]] = []
      query = t["model"].query().fetch()
      for elem in query:
        datastore[t["tag"]].append(elem.to_dict())

    utils.write_back(self,datastore)
  
