import webapp2
from string import Template
from server_controllers import models,utils

class Unsubscribe(webapp2.RequestHandler):
  def get(self,qs):
    user_id = self.request.get("user")
    hashtag = self.request.get("hashtag")
    check_hash = utils.unsubscribeHash(user_id)

    template = Template("<html><body><br><h2>$msg</h2></body></html>")

    if hashtag == check_hash:
      query = models.User.query(ancestor=models.user_key(user_id)).fetch()
      if len(query)>0:
        user = query[0]
        user.subscribed = False
        user.put()
        self.response.write(template.substitute(msg="User " + user.nickname + " was unsubscribed!"))
      else:
        self.response.write(template.substitute(msg="User not found!"))
    else:
      self.response.write(template.substitute(msg="Incorrect link"))