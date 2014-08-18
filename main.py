import os
import webapp2
import urllib
import urllib2
import json
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class RobotsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        result = urllib2.urlopen('https://spreadsheets.google.com/feeds/cells/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/basic?prettyprint=true&min-col=1&max-col=2&alt=json')
        html = result.read()
        html = json.loads(html)

        for entry in html['feed']['entry']:
            self.response.out.write( entry['content']['$t'].encode('utf-8').strip() )

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get('_escaped_fragment_')

        if fragment:
            result = urlfetch.fetch("https://spreadsheets.google.com/feeds/list/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/full?sq=uniqueid="+ urllib.quote( fragment.split('-')[0] ) +"&alt=atom")
            if result.status_code == 200:
                self.response.headers['Content-Type'] = 'application/atom+xml'
                self.response.out.write(result.content)
            else:
                self.response.status = 404
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(open('index.html','r').read())

app = webapp2.WSGIApplication([
    ('/robots.txt', RobotsPage),
    (r'/.*', IndexPage)
], debug=True)
