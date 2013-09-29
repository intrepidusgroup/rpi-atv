import sys
import SimpleHTTPServer 
import SocketServer


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('0.0.0.0', port)


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
# I hate seeing these requests all the time, so hopefully we can
# convince the browser to leave us alone
        print "Path:%s:" % self.path
        if self.path == '/favicon.ico':
            self.send_response(404)

        elif self.path.endswith("png") or self.path.endswith("jpg"):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/':
            self.path = 'index.html'
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            try:
                f = open("." + self.path)
                data = f.read()
                f.close()

                self.send_response(200)
                if self.path.endswith('xml') or self.path.endswith('plist'):
                    ct = 'application/xml'
                elif self.path.endswith('mc'):
                    ct = 'application/x-apple-aspen-config'
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

            except:
                self.send_response(404)


    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        f = open("debug.log", "a")
        f.write(post_body + "\n")
        f.close()

Handler = ServerHandler

httpd = SocketServer.TCPServer(server_address, Handler)

print "serving at port", port
httpd.serve_forever()

