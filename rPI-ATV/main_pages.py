import uuid

# front page, basically frame with top-level nav bar
#

def navigation_bar():
    out = '''

                    <viewWithNavigationBar id="PlexConnect_Navigation">
                        <navigation>
                        <navigationItem id="MovieShelf"> 
                                        <title>Movies</title> 
                                        <url>http://__HOSTNAME__/movie</url> 
                        </navigationItem> 
                        <navigationItem id="TVShelf"> 
                                        <title>TV Shows</title> 
                                        <url>http://__HOSTNAME__/tv</url> 
                         </navigationItem> 
                            <navigationItem id="About"> 
                                    <title>About</title> 
                                    <url>http://__HOSTNAME__/about</url> 
                            </navigationItem> 
                         </navigation>
                </viewWithNavigationBar>
'''
    return out


def about():
    out = '''
    <dialog id='about.panel'>
        <title>rPI ATV</title>
        <description>This is a very rough hack to put a simple media server onto a Raspberry Pi. If you can see this, congratulations! If you're
reading the code...don't. It's ugly.
        </description>
    </dialog>
'''

    return out




def add_site():

    out = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadDescription</key>
    <string>Enable Add Site</string>
    <key>PayloadDisplayName</key>
    <string>Enable Add Site</string>
    <key>PayloadIdentifier</key>
    <string>com.apple.frontrow.add_site</string>
    <key>PayloadOrganization</key>
    <string>Apple, Inc</string>
    <key>PayloadRebootSuggested</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>%(payload_uuid)s</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadIdentifier</key>
            <string>com.apple.defaults.1</string>
            <key>PayloadType</key>
            <string>com.apple.defaults.managed</string>
            <key>PayloadUUID</key>
            <string>%(content_uuid)s</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>PayloadContent</key>
            <array>
                <dict>
                    <key>DefaultsDomainName</key>
                    <string>com.apple.frontrow</string>
                    <key>DefaultsData</key>
                    <dict>
                        <key>F2BE6C81-66C8-4763-BDC6-385D39088028</key>
                        <dict>
                            <key>EnableAddSite</key>
                            <true/>
                            
                            <key>AddSiteLoggingURL</key>
                            <string>http://__HOSTNAME__/log</string>
                        </dict>
                    </dict>
                </dict>
            </array>
        </dict>
    </array>
</dict>
</plist>
''' % {'payload_uuid': str(uuid.uuid4()), 'content_uuid': str(uuid.uuid4())}

    return out



def bag_plist():
    out = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>auth-type</key>
    <string>js</string>
    <key>enabled</key>
    <string>YES</string>
    <key>menu-title</key>
    <string>Raspberry Pi</string>
    <key>merchant</key>
    <string>com.ig.atv.rpi</string>
    <key>root-url</key>
    <string>http://__HOSTNAME__/</string>
    <key>use-parental-controls</key>
    <string>YES</string>
    <key>default-parental-controls-access-level</key>
    <string>ASK</string>
    <key>menu-icon-url</key>
    <string>http://__HOSTNAME__/images/rPI.png</string>
</dict>
</plist>
'''
    return out



    


