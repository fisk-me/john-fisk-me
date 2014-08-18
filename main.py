import os
import webapp2
import urllib
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class RobotsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Robots.txt')

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get('_escaped_fragment_')

        if fragment:
            result = urlfetch.fetch("https://spreadsheets.google.com/feeds/list/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/full?sq=reference="+ urllib.quote( fragment.split('-')[0] ) +"&alt=atom")
            if result.status_code == 200:
                self.response.headers['Content-Type'] = 'application/atom+xml'
                self.response.out.write(result)
            else:
                self.response.status = 404
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(open('index.html','r').read())

app = webapp2.WSGIApplication([
    ('/robots.txt', RobotsPage),
    (r'/.*', IndexPage)
], debug=True)


