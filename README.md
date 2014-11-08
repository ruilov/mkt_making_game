# Market making game

## General design

The backend uses the [Google App Engine](https://appengine.google.com/) for hosting and its datastore for database. The backend code is in python, uses webapp2 as the framework for serving pages (Web Server Gateway Interface) and jinja2 for server side templating, although used sparingly.

The frontend is in javascript using Google's AngularJS framework which is a Single Page Application framework, meaning much of the business logic is moved to the client side. The frontend also uses Bootstrap for CSS components.

The backend servers HTML pages and also provides a number of APIs which are used for reading/writing to the database.

## Routing

- app.yaml provides the Google App Engine routing. Most requests are routed to mktmaking.py
- mktmaking.py routes the APIs as well as HTML files. Most HTML files are served by template.py
- when the URL doesn't start with domain/#/ template.py will see an empty path and serve template.html
- template.html loads up all the javascript, shows the navigation bar and uses AngularJS to route on the client side
- client side routing is implemented in template.js. This will send the client to the other htmls as appropriate.
- those other html files will also be served by template.py on the server side
- for the starting page, template.js routes to index.html which is a dummy file. 
- index.js figures out if the user is logged, in which case it forwards to /#/home, otheriwse it forwards to /#/login
- APIs data is normally passed back and forth in json format, although some parameters are passed through URL query strings

## User authentication

Gmail and facebook logins are provided.

On the server side most functions that deal with login are in utils.py and are written to handle all login providers, minimizing if-elses needed throughout the code.

The login process for gmail is easy as Google App Engine does most of the work
- template.py provides the login url, which is really provided by Google App Engine
- after login the user is forwarded to /login/gmail
- mktmaking.py routes this request to login.py, which simply makes sure that the user is saved to the datastore, then redirects to '/'
- at any time when we need the user info we can get through the users.get_current_user() service
- the logout URL is similarly provided by the GAE

Login for facebook is harder and we use the 3rd party library 'authomatic'
- template.py provides the login url, 'login/fb'
- Authomatic uses login.py for get/put requests and handles most of the process. 
- once the user is logged in, we set a cookie with user_name, user_email and user_hash
- (user_email,user_hash) then becomes the real access token, and has nothing to do with facebook. 
- there's no cookie expiration mechanism. This potentially allows user accounts to be stolen, if someone steals their cookie
- at any time when we need the user info, we retrieve from the cookie
- the logout process is handled by logout.py which deletes the cookie 