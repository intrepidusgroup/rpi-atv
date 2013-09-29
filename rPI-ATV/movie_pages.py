from urllib2 import quote
from time import localtime


global db

import media_db


def get_parade(genre=None):

    out = '<paradePreview inOrder="true">\n'


    parade = media_db.get_items(type='Movie', num_random=7, genre=genre)
    for movie in parade:
        movie['artfile'] = quote(movie['artfile'])
        out += '          <image>http://__HOSTNAME__/images/artwork/%(artfile)s</image>\n' % movie

    out += '</paradePreview>\n'

    return out


def genre_page():
    out = '''
        <listWithPreview id="com.sample.main">
      <header>
        <simpleHeader accessibilityLabel="Sample-xml main">
          <title>Genres</title>
          <image required="true">http://__HOSTNAME__/images/rPI-header.png</image>
        </simpleHeader>
      </header>

      <preview>
'''      

    out += get_parade()

    out += '''
      </preview>
      <menu>
        <sections>
          <menuSection>
            <items>
'''

    genres = media_db.list_genres()
    i = 1
    for genre_dat in genres:
        out += '''
              <oneLineMenuItem id="genre_page_%(id)s" accessibilityLabel="%(name)s" 
                  onSelect="atv.loadURL('http://__HOSTNAME__/movie/genre/%(id)s');">
                <label>%(name)s</label>
              </oneLineMenuItem>
''' % genre_dat

    out += '''
            </items>
          </menuSection>
        </sections>
      </menu>
    </listWithPreview>
    '''

    return out


def main_page():
    out = '''
        <listWithPreview id="com.sample.main">
      <header>
        <simpleHeader accessibilityLabel="Sample-xml main">
          <title>Movies!</title>
          <image required="true">http://__HOSTNAME__/images/rPI-header.png</image>
        </simpleHeader>
      </header>

      <preview>
'''      

    out += get_parade()

    out += '''
      </preview>
      <menu>
        <sections>
          <menuSection>
            <items>
              <oneLineMenuItem id="list_0" accessibilityLabel="Favorites" onSelect="atv.loadURL('http://__HOSTNAME__/movie/favorite');">
                <label>Favorites</label>
              </oneLineMenuItem>
              <oneLineMenuItem id="list_1" accessibilityLabel="Recently Added" onSelect="atv.loadURL('http://__HOSTNAME__/movie-grid.xml');">
                <label>Recently Added</label>
              </oneLineMenuItem>
              <oneLineMenuItem id="list_2" accessibilityLabel="Unwatched" onSelect="atv.loadURL('http://__HOSTNAME__/movie-grid.xml');">
                <label>Unwatched</label>
              </oneLineMenuItem>
              <oneLineMenuItem id="list_3" accessibilityLabel="Genres" onSelect="atv.loadURL('http://__HOSTNAME__/movie/genre');">
                <label>Genres</label>
              </oneLineMenuItem>
              <oneLineMenuItem id="list_4" accessibilityLabel="All" onSelect="atv.loadURL('http://__HOSTNAME__/movie/all');">
                <label>All</label>
              </oneLineMenuItem>
<!--              <oneLineMenuItem id="list_5" accessibilityLabel="Search" onSelect="atv.loadURL('http://__HOSTNAME__/movie-search.xml');">
                <label>Search</label>
              </oneLineMenuItem> -->

            </items>
          </menuSection>
        </sections>
      </menu>
    </listWithPreview>
    '''

    return out


def detail(id):
    movie = media_db.get_item(id)
    favorite = movie['favorite']
    movie['artfile'] = quote(movie['artfile'])
    out = '''
    <itemDetail id="com.sample.movie-detail">
      <title>%(title)s</title>
      <subtitle>%(studio)s</subtitle>
      <rating>%(rating)s</rating>
      <summary>%(desc)s</summary>
      <image style="moviePoster">http://__HOSTNAME__/images/artwork/%(artfile)s</image>
      <defaultImage>resource://Poster.png</defaultImage>
    ''' % movie

    cols = '''
<columnDefinition width="25" alignment="left">
<title>Details</title>
</columnDefinition>
'''
    row_data = []
    row_data.append([movie['genre']])
    if len(movie['actors']) > 0:
      row_data.append(movie['actors'].split(',')[0:4])
      cols += '''
<columnDefinition width="25" alignment="left">
<title>Actors</title>
</columnDefinition>
'''

    if len(movie['directors']) > 0:
        row_data.append(movie['directors'].split(',')[0:4])
        cols += '''
<columnDefinition width="25" alignment="left">
<title>Directors</title>
</columnDefinition>
'''
  
    if len(movie['producers']) > 0:
        row_data.append(movie['producers'].split(',')[0:4])
        cols += '''
<columnDefinition width="25" alignment="left">
<title>Producers</title>
</columnDefinition>
'''

    out += '''
    <table>
    <columnDefinitions>
    %s
    </columnDefinitions>
    <rows>
    ''' % cols


    for r in range(0,4):
        out += '<row>\n'
        for c in row_data:
            if r < len(c):
                out += '<label>%s</label>\n' % c[r]
            else:
                out += '<label/>\n'
        out += '</row>\n'

    out += '</rows>\n</table>\n'

    out += '''
<centerShelf>
<shelf id="centerShelf" columnCount="4" center="true">
<sections>
<shelfSection>
<items>

<actionButton id="play" onSelect="atv.loadURL('http://__HOSTNAME__/movie/play/%(id)s');" 
onPlay="atv.loadURL('http://__HOSTNAME__/movie/play/%(id)s');">
<title>Play</title>
<image>resource://Play.png</image>
<focusedImage>resource://PlayFocused.png</focusedImage>
<badge>HD</badge>
</actionButton>

<actionButton id="favorite" onSelect="atv.loadURL('http://__HOSTNAME__/media/toggle_favorite/%(id)s');">
<title>Favorite</title>
''' % movie

    if favorite:
      out += '''
<image>resource://WishListFocused.png</image>
<focusedImage>resource://WishList.png</focusedImage>
'''
    else:
      out += '''
<image>resource://WishList.png</image>
<focusedImage>resource://WishListFocused.png</focusedImage>
'''


    out += '''
</actionButton>

</items>
</shelfSection>
</sections>
</shelf>
</centerShelf>
''' % movie

    out += '''
<divider>
<smallCollectionDivider alignment="left">
<title>%(genre)s</title>
</smallCollectionDivider>
</divider>
<bottomShelf>
<shelf id="bottomShelf" columnCount="8">


<sections>
<shelfSection>
<items>
''' % movie

    related_movies = media_db.get_items(genre=movie['id'], num_random=8, type='Movie')

    i = 1
    for r_movie in related_movies:
        r_movie['item_id'] = i
        i += 1
        r_movie['artfile'] = quote(r_movie['artfile'])

        out += '''
<moviePoster id="%(item_id)s" accessibilityLabel="%(title)s" related="true" 
onSelect="atv.loadURL('http://__HOSTNAME__/movie/detail/%(id)s');" 
onPlay="atv.loadURL('http://__HOSTNAME__/movie/play/%(id)s')">
<title>%(title)s</title>
<image>http://__HOSTNAME__/images/artwork/%(artfile)s</image>
<defaultImage>resource://Poster.png</defaultImage>
</moviePoster>
''' % r_movie

    out += '''
</items>
</shelfSection>
</sections>
</shelf>
</bottomShelf>

'''

    out += '''
      </itemDetail>
'''


    return out


def play_movie(id):
    movie = media_db.get_item(id)
    movie['artfile'] = quote(movie['artfile'])        


    print movie['rating']
    cur_hour = localtime()[2]
    if movie['rating'] == 'R' and cur_hour < 21:
        out = '''
        <dialog id='about.panel'>
            <title>Cheap Parental Control</title>
            <description>Sorry, R-rated movies are restricted until after 9:00 pm. 
            </description>
        </dialog>
        '''

    else:
        out = '''
            <videoPlayer id="com.sample.video-player">
                    <httpFileVideoAsset id="%(id)s">
                            <mediaURL>http://__HOSTNAME__/media/play/%(id)s</mediaURL>
                            <title>%(title)s</title>
                            <description>%(desc)s</description>
                            <image>%(artfile)s</image>
                            <rating>%(rating)s</rating>
                    </httpFileVideoAsset>
            </videoPlayer>
    ''' % movie

    return out

def film_grid(genre=None, recent=None, unwatched=None, favorite=False, title='Movies'):

    out = '''
    <scroller id="com.sample.movie-grid">
      <header>
        <simpleHeader accessibilityLabel="Simple Movies">
          <title>%s</title>
          <image required="true">http://__HOSTNAME__/pi/images/DASnet-atv.png</image>
        </simpleHeader>
      </header>
      <items>
        <grid id="grid_0">
          <items>
    ''' % title

    movies = media_db.get_items('Movie', genre=genre, favorite=favorite)

    i = 0
    for movie in movies:
        i += 1
        movie['item_num'] = i
        movie['artfile'] = quote(movie['artfile'])        
        out += '''
            <moviePoster id="grid_item_%(item_num)s" accessibilityLabel="%(title)s" 
                onSelect="atv.loadURL('http://__HOSTNAME__/movie/detail/%(id)s');" 
                onPlay="atv.loadURL('http://__HOSTNAME__/movie/play/%(id)s');">
              <title>%(title)s</title>
              <image>http://__HOSTNAME__/images/artwork/%(artfile)s</image>
              <defaultImage>resource://Poster.png</defaultImage>
            </moviePoster>
        ''' % movie



    out += '''
          </items>
        </grid>
      </items>
    </scroller>
'''
    return out
