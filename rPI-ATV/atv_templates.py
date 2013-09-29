

def wrap_page(content):
    out = '''<?xml version="1.0" encoding="UTF-8"?>
<atv>
  <head>
      <script src="http://__IP_ADDR__/js/item-detail.js"/>
  </head>
  <body>
'''
    out += content

    out += '''  </body>
</atv>'''
    return out


def movie_item(item_data):

    item_data['logo'] = 'URL for app logo'

    out = '''
    <itemDetail id="com.sample.movie-detail">
      <title>%(title)s</title>
      <rightImage required="true">%(logo)s</rightImage>
      <rating>%(rating)s</rating>
      <summary>%(desc)s</summary>
      <image style="moviePoster">%(artfile)s</image>
      <defaultImage>resource://Poster.png</defaultImage>
    ''' % (item_data)


    cols = ['Details']
    coldata = []
    coldata.append([item_data['genre'],  "Released %s" % item_data['year'], 
        "%d minutes" % item_data['running_time']])
    tallest = 3

    actors = item_data.get('actors')
    if actors != None:
        cols.append('Actors')
        a = actors.split(',')
        coldata.append(a)
        if len(a) > tallest:
            tallest = len(a)


    directors = item_data.get('directors')
    if directors != None:
        cols.append('Directors')
        d = directors.split(',')
        coldata.append(d)
        if len(d) > tallest:
            tallest = len(d)


    producers = item_data.get('producers')
    if producers != None:
        cols.append('Producers')
        p = producers.split(',')
        coldata.append(p)
        if len(p) > tallest:
            tallest = len(p)

    out += '''
      <table>
        <columnDefinitions>
'''

    for col in cols:
        out += '''
          <columnDefinition width="25" alignment="left">
            <title>%s</title>
          </columnDefinition>
''' % col

    out += '''
        </columnDefinitions>
        <rows>
'''

    for i in range(0, tallest):
        out += '          <row>\n'
        for col in coldata:
            if i >= len(col):
                out += '            <label/>\n'
            else:
                out += '            <label>%s</label>\n' % col[i].strip()
        out += '          </row>\n'

    out += '''
        </rows>
      </table>
'''


    out += '    </itemDetail>\n'

    page = wrap_page(out)

    return page


def navigation_bar():
    out = '''

                    <viewWithNavigationBar id="PlexConnect_Navigation">
                        <navigation>
                        <navigationItem id="MovieShelf"> 
                                        <title>Movies</title> 
                                        <url>http://__IP_ADDR__/pi/movie-main.xml</url> 
                        </navigationItem> 
                        <navigationItem id="TVShelf"> 
                                        <title>TV Shows</title> 
                                        <url>http://__IP_ADDR__/pi/tv-main.xml</url> 
                         </navigationItem> 
                            <navigationItem id="UITest"> 
                                    <title>UI Test</title> 
                                    <url>http://__IP_ADDR__/sample-main.xml</url> 
                            </navigationItem> 
                         </navigation>
                </viewWithNavigationBar>
'''
    return out




