import webapp2,os,jinja2

# this is the controller for all HTML pages

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("./"),
  extensions=['jinja2.ext.autoescape'],
  variable_start_string='((', 
  variable_end_string='))',
  autoescape=True
)

class HTMLServer(webapp2.RequestHandler):
  def get(self,path):
    resolved_path = "template.html"
    if(path!=""): resolved_path = path
    template_values = {}
    template = JINJA_ENVIRONMENT.get_template("html/"+resolved_path)
    self.response.write(template.render(template_values))

