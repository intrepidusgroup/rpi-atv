import re

import cherrypy
from cherrypy.lib.static import serve_file

import main_pages, movie_pages
import media_db


MY_HOSTNAME = '192.168.37.20:80'
PORT=80

db = None

# cherry py / restful stuff - helpful comments found here: 
#   http://stackoverflow.com/questions/2715227/cherrypy-and-restful-web-api


# url structure:
# main - front page, navigation bar
# main/movie - main movie page (with selection menu)
# main/tv - same but for tv
# favorites/movies - 
# all/movies
# genre/movies/<genre-id>
# etc.
#
# feels backwards, but this lets us re-use favorite, all, etc.
#
# otoh, there'll be a lot of differences between movie & tv anyway...probably
# best just to have them as different targets.
#
# /movie/ - main movie page
# /movie/genre - list genres
# /movie/genre/x - list movies in genre id x
# 


class Movies(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self, command = None, id = None):
        if command == None:
            print '\n** Main movie page\n'
            return send_page(self, movie_pages.main_page())

        elif command == 'genre':
            if id == None:
                print '\n** Listing all genres\n'
                return send_page(self, movie_pages.genre_page())

            else:
                print '\n** Listing all movies in genre ID: %s\n' % id
                title = media_db.get_genre_name(id)
                return send_page(self, movie_pages.film_grid(genre=id, title=title))

        elif command == 'favorite':
            print '\n** Listing favorite movies\n'
            return send_page(self, movie_pages.film_grid(favorite=True, title='Favorites'))

        elif command == 'all':
            print '\n** Listing all movies\n'
            return send_page(self, movie_pages.film_grid())

        elif command == 'detail':
            print '\n** Movie detail, id %s' % id
            return send_page(self, movie_pages.detail(id))

        elif command == 'play':
            print '\n** Play movie id %s' % id
            return send_page(self, movie_pages.play_movie(id))


class TV(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self, command = None, id = None, sub = None):
        if command == None:
            print '\n** Main tv page\n'
        
        elif command == 'genre':
            if id == None:
                print '\n** Listing all genres\n'
                return send_page(self, movie_pages.list_genres())

            else:
                if sub == 'preview':
                    print '\n** hovering over genre, update parade'
                else:
                    print '\n** Listing all tv shows in genre ID: %s\n' % id

        elif command == 'all':
            print '\n** Listing all tv shows\n'


class Media(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self, command = None, id = None):
        if id == None:
            print "\n** Playing media, but no id received\n"
        
        elif command == 'play':
            media = media_db.get_item(id)
            filename = media['filename']

            return serve_file(filename, content_type = 'video/mp4')

        elif command == 'toggle_favorite':
            print "\n** Toggling favorite for media id %s" % id
            media_db.toggle_favorite(id)
            return send_page(self, movie_pages.detail(id))


class About(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self):
        print '\n** Displaying about page\n'
        return send_page(self, main_pages.about())


class Root(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self):
        print '\n** Displaying main page\n'
        return send_page(self, main_pages.navigation_bar())



class ATV(object):
    exposed = True
    def __init__(self):
        pass

    def GET(self, page=None):
        if page == None:
            print '\n** Need to put an about page here\n'

        elif page == 'addsite.mc':
            print '\n** serving add site profile\n'
            return send_page(self, main_pages.add_site(), wrap=False)

        elif page == 'bag.plist':
            print '\n** serving bag.plist\n'
            return send_page(self, main_pages.bag_plist(), wrap=False)


class Log(object):
    exposed = True
    def __init__(self):
        pass

    def POST(self, **params):
#        content_len = int(cherrypy.request.headers['Content-Length'])
#        post_body = cherrypy.request.body.read(50)
#        print "B: %s" % post_body

#        content_len = int(self.headers.getheader('content-length'))
#        print "L: %d" % content_len
#        print "P: %s" % params
#        post_body = self.rfile.read(content_len)
        body = params.keys()[0]
        f = open("error.log", "a")
        f.write(body + "\n")
        f.close()


def send_page(request, content, wrap=True):
    if wrap:
        content = wrap_page(content)
    content = re.sub('__HOSTNAME__', MY_HOSTNAME, content)

    cherrypy.response.status = 200
    cherrypy.response.headers['Content-type'] = 'text/xml'
    cherrypy.response.headers['Content-length'] = len(content)

    return content



def wrap_page(content):
    out = '''<?xml version="1.0" encoding="UTF-8"?>
<atv>
  <body>
'''
    out += content

    out += '''  </body>
</atv>'''

    out = re.sub('&', '&amp;', out)
    return out




def main():
    global db

    root = Root()
    root.movie = Movies()
    root.tv = TV()
    root.about = About()
    root.media = Media()
    root.atv = ATV()
    root.log = Log()

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': PORT,
            'tools.staticdir.root': '/Users/dschuetz/Work/AppleTV/rPI',
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'images',
        }
    }

    cherrypy.quickstart(root, '/', conf)


if __name__ == '__main__':
    main()
