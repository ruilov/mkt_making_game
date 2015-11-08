import webapp2
from server_apis import *
from server_controllers import *

application = webapp2.WSGIApplication([
  ('/api/lookup/',lookup.Lookup),
  (r'/api/quiz_status_update/(.*)',quiz_status_update.QuizStatusUpdate),
  ('/api/save_quiz_editor/',save_quiz_editor.SaveQuizEditor),
  ('/api/quiz_submit/',quiz_submit.QuizSubmit),
  ('/api/rate_question/',rate_question.RateQuestion),
  ('/api/suggestion/',suggestion.Suggestion),
  ('/api/sendmail/',sendmail.Sendmail),
  (r'/api/datastore_ops/(.*)',datastore_ops.DatastoreOps),
  webapp2.Route(r'/login/<:.*>', login.Login, handler_method='any'),
  ('/logout/',logout.Logout),
  (r'/unsubscribe/(.*)',unsubscribe.Unsubscribe),
  (r'/(.*)', html_server.HTMLServer),
], debug=True)