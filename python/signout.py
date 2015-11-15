import webapp2

class SignOut(webapp2.RequestHandler):
  def get(self):
    self.response.delete_cookie('username')
    self.response.delete_cookie('hash')
    self.redirect('/')