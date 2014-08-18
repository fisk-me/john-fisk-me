import os
import webapp2
import urllib
import urllib2
import json
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class RobotsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write( "User-Agent: *\n" )
        self.response.out.write( "Disallow:\n" )

        result = urllib2.urlopen("https://spreadsheets.google.com/feeds/cells/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/basic?prettyprint=true&min-col=1&max-col=2&alt=json")
        html = result.read()
        html = json.loads(html)

        for entry in range(1,len(html["feed"]["entry"])/2):
            self.response.out.write( "Allow: /#!" + html["feed"]["entry"][entry*2]["content"]["$t"].encode("utf-8").strip() + "-" + urllib.quote(html["feed"]["entry"][entry*2+1]["content"]["$t"].encode("utf-8").strip()) +"\n" )

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get("_escaped_fragment_")

        if fragment:
            result = urllib2.urlopen("https://spreadsheets.google.com/feeds/list/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/full?sq=uniqueid="+ urllib.quote( fragment.split("-")[0] ) +"&alt=atom")
            if result.getcode() == 200:
                self.response.headers["Content-Type"] = "application/atom+xml"
                self.response.out.write(result.read())
            else:
                self.response.status = 404
        else:
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(open("index.html","r").read())

app = webapp2.WSGIApplication([
    ("/robots.txt", RobotsPage),
    (r"/.*", IndexPage)
], debug=True)
