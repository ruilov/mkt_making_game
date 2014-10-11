import webapp2
import datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

# this API is for admins of the site to create quizzes

class QuizEditor(webapp2.RequestHandler):
  def get(self,idStr):    
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)
    jsonStr = simplejson.dumps(quiz.to_dict(), cls = utils.MyEncoder)
    self.response.out.write(jsonStr)

  def post(self,idStr):
    quiz_id = self.request.get("id")
    quiz = models.getQuiz(quiz_id)

    # parse the json into a model quiz. There's probably an easier way to do this
    json = simplejson.loads(self.request.body)
    questionArr = []
    for questionJSON in json["questions"]:
      question = models.Question()
      question.text = questionJSON["text"]
      question.source = questionJSON["source"]
      question.answer = questionJSON["answer"]
      questionArr.append(question)
    quiz.questions = questionArr
    quiz.status = "editor"
    quiz.put()



    