import webapp2,os,jinja2,urllib
from server_controllers import models,utils

from authomatic.adapters import Webapp2Adapter
from auth_config import authomatic

class Login(webapp2.RequestHandler):
  # The handler must accept GET and POST http methods and
  # Accept any HTTP method and catch the "provider_name" URL variable.
  def any(self, provider_name):
    if provider_name == "fb":
      result = authomatic.login(Webapp2Adapter(self), provider_name)
      # Do not write anything to the response if there is no result!
      if result:
        # If there is result, the login procedure is over and we can write to response.
        if result.error:
          # Login procedure finished with an error.
          self.response.set_cookie('error', urllib.quote(result.error.message))
          self.response.delete_cookie('user_name')
          self.response.delete_cookie('user_email')
          self.response.delete_cookie('user_hash')
          self.redirect('/')
        elif result.user:
          # Hooray, we have the user!
          result.user.update()
          self.response.set_cookie('user_name', urllib.quote(result.user.name))
          self.response.set_cookie('user_email', urllib.quote(result.user.email))
          self.response.set_cookie('user_hash', urllib.quote(utils.userHash(result.user.email)))
          self.response.delete_cookie('error')
          self.redirect('/login/fb2')

    elif provider_name == "fb2":
      models.check_user_in_db(self)
      self.redirect('/')

    elif provider_name == "gmail":
      models.check_user_in_db(self)
      self.redirect('/')
