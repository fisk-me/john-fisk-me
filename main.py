import os
import webapp2
import urllib
import urllib2
import json
from google.appengine.ext.webapp import template

class SitemapPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        result = urllib2.urlopen("https://spreadsheets.google.com/feeds/cells/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/basic?prettyprint=true&min-col=1&max-col=2&alt=json")
        data = json.loads(result.read())
        for entry in range(1,len(data["feed"]["entry"])/2):
            self.response.out.write( "http://john.fisk.me/#!" + data["feed"]["entry"][entry*2]["content"]["$t"].encode("utf-8").strip() + "-" + urllib.quote(data["feed"]["entry"][entry*2+1]["content"]["$t"].encode("utf-8").strip()) +"\n" )

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get("_escaped_fragment_") + "-"

        if fragment:
            result = urllib2.urlopen("https://spreadsheets.google.com/feeds/list/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/full?sq=uniqueid="+ urllib.quote( fragment.split("-")[0] ) +"&prettyprint=true&alt=json")
            if result.getcode() == 200:
                data = json.loads(result.read())
                self.response.headers["Content-Type"] = "text/html"
                self.response.out.write(template.render(os.path.join(os.path.dirname(__file__),"entry.tmpl"), data))
            else:
                self.response.status = 404
        else:
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(open("index.html","r").read())

app = webapp2.WSGIApplication([
    ("/sitemap.txt", SitemapPage),
    (r"/.*", IndexPage)
], debug=True)
