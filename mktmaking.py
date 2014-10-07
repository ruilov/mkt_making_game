import webapp2
from server_controllers import main,quizzes,quiz_editor,login

application = webapp2.WSGIApplication([
  ('/login/',login.MyHandler),
  ('/quizzes_api/',quizzes.Quizzes),
  (r'/quiz_editor_api/(.*)',quiz_editor.QuizEditor),
  (r'/(.*)', main.MainPage),
], debug=True)