import webapp2
from google.appengine.ext.webapp import template

class RobotsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Robots.txt')

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get('_escaped_fragment_')

        if fragment:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write( fragment )
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(template.render('index.html', None))

app = webapp2.WSGIApplication([
    ('/robots.txt', RobotsPage),
    (r'/.*', IndexPage)
], debug=True)
