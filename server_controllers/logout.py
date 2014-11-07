import webapp2

class Logout(webapp2.RequestHandler):
  def get(self):
    self.response.delete_cookie('user_name')
    self.response.delete_cookie('user_email')
    self.response.delete_cookie('user_hash')
    self.response.delete_cookie('error')
    self.redirect('/')
    