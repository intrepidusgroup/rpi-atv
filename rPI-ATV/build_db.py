import re, sys, os, os.path
import subprocess
import xml.etree.ElementTree as ET
import plistlib
import media_db


#VIDEO_DIR = '/Volumes/Data/Video/copied'
VIDEO_DIR = '/Volumes/ExtMedia/TV'
MP4_INFO = '/usr/local/bin/AtomicParsley'
MP4_CMD = '--outputXML'



#
# tags we want: 
#   Name
#   Artist (take 1st four on list)
#   Release Date (take 1st 4 chars -- year)
#   Long Dexcription


#    c.execute('''CREATE TABLE media (id integer primary key, type text,
#        title text, desc text, rating_num integer, rating text, 
#        year integer, filename text, artfile text, genre text,
#        running_time integer, actors text, directors text, 
#        producers text)''')


def parse_tags(data, filename, artwork):
    tree = ET.fromstring(data)

    tag_data = {'type': 'Movie', 'filename': filename, 'artfile': artwork}
    for atom in tree[0]:
        key = atom.attrib['name']
        try:
            value = atom.attrib['value']
        except:
            value = atom.text


        if value != None:
            if key[1:] == 'nam':
                tag_data['title'] = value

            elif key[1:] == 'ART':
                if 'actors' not in tag_data:
                    tag_data['actors'] = value

            elif key[1:] == 'gen':
                tag_data['genre'] = value

            elif key[1:] == 'day':
                tag_data['year'] = value[0:4]

            elif key == 'desc' and 'desc' not in tag_data:
                tag_data['desc'] = value

            elif key == 'ldes':
                tag_data['desc'] = value

            elif key == '----':
                if re.match('.+\|.*\|.+\|', value):
                    std, rating, rating_num, dum = value.split('|')
                    tag_data['rating'] = rating
                    tag_data['rating_num'] = rating_num
                elif 'plist' in value:
                    pl = plistlib.readPlistFromString(value.encode('utf-8'))

                    if 'cast' in pl:
                        tag_data['actors'] = pull_names(pl['cast'])

                    if 'directors' in pl:
                        tag_data['directors'] = pull_names(pl['directors'])

                    if 'producers' in pl:
                        tag_data['producers'] = pull_names(pl['producers'])

                    if 'studio' in pl:
                        tag_data['studio'] = pull_names(pl['studio'])


    media_db.add_item(tag_data)


def pull_names(names):
    if isinstance(names, basestring):
        return names

    t = []
    for a in names:
         t.append(a['name'])
    return ','.join(t)


def read_file(filename):
    if filename[-4:] == '.m4v':

        print filename
        proc = subprocess.Popen([MP4_INFO, filename, '-E'],   # extract artwork
            stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()

        artwork = out.split('/')[-1:][0].strip()
        print "   %s" % artwork

        proc = subprocess.Popen([MP4_INFO, filename, MP4_CMD], 
            stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        parse_tags(out, filename, artwork)



def main():
    for root, dum, files in os.walk(VIDEO_DIR):
        for file in files:
            filename = os.path.join(root, file)
            read_file(filename)



if __name__ == '__main__':
    main()
