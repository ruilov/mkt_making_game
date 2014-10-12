import webapp2
from server_controllers import template,api_quizzes,api_quiz_editor,api_quiz,api_scores,api_is_logged

application = webapp2.WSGIApplication([
  ('/is_logged_api',api_is_logged.IsLogged),
  (r'/scores_api/(.*)',api_scores.Scores),
  (r'/quizzes_api/(.*)',api_quizzes.Quizzes),
  (r'/quiz_api/(.*)',api_quiz.Quiz),
  (r'/quiz_editor_api/(.*)',api_quiz_editor.QuizEditor),
  (r'/(.*)', template.TemplatePage),
], debug=True)