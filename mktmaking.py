import webapp2
from server_controllers import main,quizzes,quiz_editor

application = webapp2.WSGIApplication([
  ('/quizzes_api/',quizzes.Quizzes),
  (r'/quiz_editor_api/(.*)',quiz_editor.QuizEditor),
  (r'/(.*)', main.MainPage),
], debug=True)