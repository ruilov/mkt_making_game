import webapp2
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
  # loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class MainPage(webapp2.RequestHandler):
  def get(self,path):
    template_path = "index.html"
    if(path!=""): template_path = path

    template_values = {}

    template = JINJA_ENVIRONMENT.get_template("html/"+template_path)
    self.response.write(template.render(template_values))