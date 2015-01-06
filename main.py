import os
import webapp2
import urllib
import urllib2
import json
from google.appengine.ext.webapp import template

class SitemapPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write( "http://john.fisk.me/" )
        result = urllib2.urlopen("https://spreadsheets.google.com/feeds/cells/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/basic?prettyprint=true&min-col=1&max-col=2&alt=json")
        data = json.loads(result.read())
        for entry in range(len(data["feed"]["entry"])/2,1,-1):
            self.response.out.write( "http://john.fisk.me/#!" + data["feed"]["entry"][entry*2]["content"]["$t"].encode("utf-8").strip() + "-" + urllib.quote(data["feed"]["entry"][entry*2+1]["content"]["$t"].encode("utf-8").strip()) +"\n" )
            
class SitemapPage2(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("<html><head><title>john.fisk.me sitemap</title></head><body>");
        result = urllib2.urlopen("https://spreadsheets.google.com/feeds/cells/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/basic?prettyprint=true&min-col=1&max-col=2&alt=json")
        data = json.loads(result.read())
        for entry in range(len(data["feed"]["entry"])/2,1,-1):
            self.response.out.write( "<a href='http://john.fisk.me/#!" + data["feed"]["entry"][entry*2]["content"]["$t"].encode("utf-8").strip() + "-" + urllib.quote(data["feed"]["entry"][entry*2+1]["content"]["$t"].encode("utf-8").strip()) +"'>"+data["feed"]["entry"][entry*2+1]["content"]["$t"].encode("utf-8").strip()+"</a><br />\n" )
        self.response.out.write("</body></html>")

class IndexPage(webapp2.RequestHandler):
    def get(self):
        fragment = self.request.get("_escaped_fragment_")

        if fragment:
            result = urllib2.urlopen("https://spreadsheets.google.com/feeds/list/1-duH2HS3Y_mjbXRib3mxzjwaxfPmZ7QQvVcqwH_jeZQ/1/public/full?sq=uniqueid="+ urllib.quote( (fragment+"-").split("-")[0] ) +"&prettyprint=true&alt=json")
            if result.getcode() == 200:
                data = json.loads(result.read())
                for entry in data["feed"]["entry"]:
                    entryData = dict( [ (k[4:], v['$t']) for k, v in entry.items() if "gsx$" in k ] )
                self.response.headers["Content-Type"] = "text/html"
                self.response.out.write(template.render(os.path.join(os.path.dirname(__file__),"entry.tmpl"), entryData))
            else:
                self.response.status = 404
        else:
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write(open("index.html","r").read())

app = webapp2.WSGIApplication([
    ("/sitemap.txt", SitemapPage),
    ("/sitemap.html", SitemapPage2),
    (r"/.*", IndexPage)
], debug=True)
