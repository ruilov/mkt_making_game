import webapp2
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models

class QuizEditor(webapp2.RequestHandler):
  def get(self,idStr):    
    quiz_id = self.request.get("id")
    quiz = getQuiz(quiz_id)
    jsonStr = simplejson.dumps({"quiz": quiz.to_dict()})
    self.response.out.write(jsonStr)

  def post(self,idStr):
    quiz_id = self.request.get("id")
    quiz = getQuiz(quiz_id)

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

    quiz.put()

def getQuiz(quiz_id):
  query = models.Quiz.query(ancestor=models.quiz_key(quiz_id))
  response = query.fetch(1)

  if(len(response)==0):
    quiz = models.Quiz(parent=models.quiz_key(quiz_id))
  else:
    quiz = response[0]

  return quiz

    