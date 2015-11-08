import webapp2,urllib
from string import Template
import utils

class Unsubscribe(webapp2.RequestHandler):
  def get(self,qs):
    user_email = urllib.quote(self.request.get("user"))
    hashtag = self.request.get("hashtag")
    check_hash = utils.unsubscribeHash(user_email)

    template = Template("<html><body><br><h2>$msg</h2></body></html>")

    if hashtag == check_hash:
      user_email = urllib.unquote(user_email)
      query = models.User.query(models.User.email==user_email).fetch()
      if len(query)>0:
        user = query[0]
        user.subscribed = False
        user.put()
        self.response.write(template.substitute(msg="User " + user.name + " was unsubscribed!"))
      else:
        self.response.write(template.substitute(msg="User not found!"))
    else:
      self.response.write(template.substitute(msg="Incorrect link"))