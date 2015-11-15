import webapp2

class SignOut(webapp2.RequestHandler):
  def get(self):
    self.response.delete_cookie('id')
    self.response.delete_cookie('hash')
    self.redirect('/')