# Simple mkt making app

## General design

The backend uses the [Google App Engine](https://appengine.google.com/) for hosting and its datastore for storage. The code is in python, uses webapp2 as the framework for serving pages (Web Server Gateway Interface) and jinja2 for server side templating, although used sparingly.

The frontend is in javascript using Google's AngularJS framework which is Single Page Application framework, meaning much of the business logic is moved to the client side. The frontend also uses Bootstrap for CSS components.

The backend servers HTML pages and also provides a number of APIs

The flow of info is:
- app.yaml provides the Google App Engine routing. Most requests are routed to mktmaking.py
- 
