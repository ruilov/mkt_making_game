import webapp2
from python import *

application = webapp2.WSGIApplication([
  ('/api/lookup/',lookup.Lookup),
  ('/api/signup/',signup.SignUp),
  ('/api/signin/',signin.SignIn),
  ('/api/signout/',signout.SignOut),
  ('/api/reset/',reset.Reset),
  (r'/reset/(.*)',reset.Reset),
  ('/api/quiz_status_update/',quiz_status_update.QuizStatusUpdate),
  ('/api/save_quiz_editor/',save_quiz_editor.SaveQuizEditor),
  ('/api/quiz_submit/',quiz_submit.QuizSubmit),
  ('/api/rate_question/',rate_question.RateQuestion),
  ('/api/suggestion/',suggestion.Suggestion),
  ('/api/sendmail/',sendmail.Sendmail),
  (r'/api/datastore_ops/(.*)',datastore_ops.DatastoreOps),
  (r'/unsubscribe/(.*)',unsubscribe.Unsubscribe),
  (r'/(.*)', html_server.HTMLServer),
], debug=True)