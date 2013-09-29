#
# really rough "proxy" server to process AppleTV data and push back to the
# browser as html.
# 
# an ugly hack, even when you don't consider all the cruft that's left in here
# from the way I wrote it.
#
# the cool bits here aren't even in the code -- it's the CSS and XSLT magic.
#
import re, sys
import BaseHTTPServer
import SimpleHTTPServer 
import SocketServer, logging, cgi

from lxml import etree
import urllib2
from urlparse import urlparse


#
# because I was lazy, this is pretty stupid
# you need to set your machine's IP address here
#

#my_ip = '192.168.1.37'
my_ip = '172.20.3.162'

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('0.0.0.0', port)


main_xsl = ''


def xslt_transform(xsl_sheet, data):
    f = open('atv.xsl')
    xsl_sheet = f.read()
    f.close()

    transform = etree.XSLT(etree.XML(xsl_sheet))
    doc = etree.XML(data)
    result = transform(doc)
    print str(result)

    return str(result)

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        #logging.error(self.headers)

        if self.path == '/':
            self.path = '/main.xml'

        if self.path == '/favicon.ico':
            self.send_response(404)

        elif self.path.startswith('/http'):
            print "Path: %s" % self.path
            remote_url = self.path[1:]
            req = urllib2.Request(remote_url, None, {'User-Agent': 'Mozilla 5.10'})
            resp = urllib2.urlopen(req)
            data = resp.read()
            self.send_response(200)
            barePath = urlparse(self.path).path
            if self.path.endswith('xml') or self.path.endswith('atv') or barePath.endswith('xml') or 'XML' in resp.headers['Content-type'].upper():
                data = xslt_transform(main_xsl, data)
                data = re.sub('http://', 'http://%s:%d/http://' % (my_ip, port), data)
                data = re.sub('https://', 'http://%s:%d/https://' % (my_ip, port), data)
                self.send_header('Content-type', 'text/html')
            elif self.path.endswith('js'):
                data = re.sub('http://', 'http://%s:%d/http://' % (my_ip, port), data)
                data = re.sub('https://', 'http://%s:%d/https://' % (my_ip, port), data)                
                self.send_header('Content-type', 'application/javascript')
            elif self.path.endswith('png'):
                self.send_header('Content-type', 'image/png')
            else:
                self.send_header('Content-type', 'text/plain')

            self.send_header('Content-length', len(data))
            self.end_headers()
            self.wfile.write(data)

        elif self.path.endswith("png") or self.path.endswith("jpg"):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


        elif self.path.endswith('.xml'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')

            f = open("." + self.path)
            data = f.read()
            data = re.sub('http://', 'http://%s:%d/http://' % (my_ip, port), data)
            my_content = xslt_transform(main_xsl, data)

            self.send_header('content-length', len(my_content))
            self.end_headers()

            self.wfile.write(my_content)


        else:
            try:
                f = open("." + self.path)
                data = f.read()
                data = re.sub('__IP_ADDR__', my_ip, data)

                self.send_response(200)
                if self.path.endswith('xml') or self.path.endswith('plist') or self.path.endswith('mc'):
                    ct = 'application/xml'
                elif self.path.endswith('js'):
                    ct = 'application/js'
                elif self.path.endswith('txt'):
                    ct = 'text/plain'
                elif self.path.endswith('css'):
                    ct = 'text/css'
                else:
                    ct = 'text/html'
                self.send_header('Content-type', ct)
                self.end_headers()
                self.wfile.write(data)
                f.close()

            except:
                self.send_response(404)


    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        f = open("error.log", "a")
        f.write(post_body + "\n")
        f.close()
        #print post_body
        #for item in form.list:
        #    logging.error(item)
        #SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(server_address, Handler)

print "serving at port", port
httpd.serve_forever()

