import sqlite3
import random

import os.path
global conn

DB_NAME='media.db'

conn = None


# should add studio field

media_fields = ['id', 'type', 'title', 'desc', 'rating_num', 'rating', 
        'year', 'filename', 'artfile', 'genre', 'running_time',
        'actors', 'directors', 'producers', 'studio', 'favorite']


def connect_db( filename=DB_NAME):
    global conn
    if os.path.isfile(filename):
        conn = sqlite3.connect(filename)
        conn.text_factory = str

    else:
        initialize_db(filename)


def initialize_db( filename):
    global conn

    conn = sqlite3.connect(filename)
    conn.text_factory = str

    c = conn.cursor()

    c.execute('CREATE TABLE types (id integer primary key, name text)')
    for media_type in ['Movie', 'TV', 'Music']:
        c.execute('INSERT INTO types (name) VALUES (?);', [media_type])

    c.execute('''CREATE TABLE media (id integer primary key, type text,
        title text, desc text, rating_num integer, rating text, 
        year integer, filename text, artfile text, genre text,
        running_time integer, actors text, directors text, 
        producers text, studio text, favorite boolean)''')

    conn.commit()


def get_types():
    connect_db()
    c = conn.cursor()
    c.execute('SELECT name FROM types ORDER BY name')
    types = []
    for r in c.fetchall():
        types.append(r[0])
    return types


def add_item( data):
    connect_db()
    '''adds item to database. parameter 'data' is a dict:
        {'type': 'movie', 'title': 'Star Wars', 'genre': 'SciFi / Fantasy',
        'desc': 'Describe the movie', 'rating_num': 200, 'rating': 'PG',
        'year': 1977, 'filename': 'starwars.mp4', 'artfile': 'starwars.png'}
    etc.'''

    parms = []
    cols = []

    for f in media_fields:
        if f in data:
            parms.append(data[f])
            cols.append(f)

    cmd = "INSERT INTO media (%s) VALUES (%s?)" % (', '.join(cols), '?,' * (len(cols)-1))
    c = conn.cursor()
    c.execute(cmd, parms)
    conn.commit()


def get_item(id):
    connect_db()
    parms = []

    cmd = "SELECT %s FROM media WHERE id=?" % (', '.join(media_fields))

    c = conn.cursor()
    c.execute(cmd, [id])
    conn.commit()

    r = c.fetchall()[0]
    i = 0
    result = {}
    for f in media_fields:
        result[f] = r[i]
        i += 1

    return result


def parse_item_data(row):
    item = {}

    i = 0
    for f in media_fields:
        item[f] = row[i]
        i += 1

    return item


def list_genres():
    connect_db()

    cmd = 'SELECT id, genre, count(genre) FROM media GROUP BY genre ORDER BY genre'
    c = conn.cursor()
    c.execute(cmd, [])
    result = []
    for row in c.fetchall():
        result.append({'name': row[1], 'id': row[0]})

    return result


def toggle_favorite(id=0):
    connect_db()

    cmd = 'SELECT favorite FROM media WHERE id = ?'
    c = conn.cursor()
    c.execute(cmd, [id])
    r = c.fetchone()
    if r[0] != None:
        print "Data: %s" % r[0]
        if r[0] == 1:

            fav = 0
        else:
            fav = 1
    else:
        fav = 1

    print "New favorite: %d" % fav
    cmd = 'UPDATE media SET favorite = ? WHERE id = ?'
    c.execute(cmd, [fav, id])
    conn.commit()

    return 


def get_genre_name(id=0):
    if id != 0 and id != None:
        connect_db()
        cmd = 'SELECT genre FROM media WHERE id = ?'
        c = conn.cursor()
        c.execute(cmd, [id])
        r = c.fetchone()
        genre = r[0]

        return genre
    else:
        return None

def get_items(type='Movie', num_random=0, genre=0, favorite=False):
    connect_db()

    genre = get_genre_name(id=genre)

    result = []
    if num_random == 0:
        cmd = 'SELECT * FROM media WHERE type=?'
        parms = [type]
        if genre != None:
            cmd += 'AND genre=?'
            parms.append(genre)

        if favorite == True:
            cmd += 'AND favorite=1'

        c = conn.cursor()
        c.execute(cmd, parms)

        for row in c.fetchall():
            result.append(parse_item_data(row))

    else:
        c = conn.cursor()
        c.execute('SELECT max(id) from media WHERE type=?', [type])
        r = c.fetchone()
        m_id = r[0]

        for i in range(0, num_random):
            found = 0
            while not found:
                id = random.randrange(m_id)
                parms = [type, id]
                cmd = 'SELECT * FROM media WHERE type=? and id=?'
                if genre != None:
                    cmd += 'AND genre=?'
                    parms.append(genre)

                c = conn.cursor()
                c.execute(cmd, parms)
                r = c.fetchone()
                if r != None:
                    if r[1] == type:
                        found = 1

            result.append(parse_item_data(r))


    return result

# should we be using the iTunes-style rating string: 'mpaa|pg|200|mild this and that'?




def main():

    db = media_db('test.db')



if __name__ == '__main__':
    main()
