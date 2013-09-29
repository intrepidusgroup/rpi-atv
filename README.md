# Raspberry Pi server on Apple TV

## Table of Contents
* Introduction
* How to do it
* What's here
    * Quickstart
    * Simulator
    * Raspberry Pi AppleTV Server
    * DerbyCon Slides
* Caveats
* Acknowledgements


## Introduction

While I've had AppleTVs for years (since shortly after the first, non-iOS units were introduced), I hadn't really looked into how they worked until recently. One question I had was: How do developers test the applications they write for the AppleTV? Because there had to be developers...I didn't really think Apple was writing the 3rd party channel apps...

Turns out, it's pretty easy. And the apps aren't really apps, they're more like channels, or data feeds...or something. 

In early June, 2013, after being inspired by the PlexConnect hack to identify and document the exact mechanism (where, why, and how) for adding apps, I spent a week digging through configuraiton files, property lists, application binaries, and tearing things apart in IDA pro. The result of all this hacking was a talk I gave at DerbyCon 3.0 on September 29, 2013, and the slides, (ROUGH!) code, and general documetation you see here.


## How to do it

It's really quite simple: Just load a configuration profile that adds the "Add Site" button to the main AppleTV screen. The trick is figuring the right key to use -- Apple hid it under a (simple) layer of obfuscation.

Basically, you need a .mobileconfig profile that includes the following payload:


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
                    <string>http://my.server.com/log</string>
                </dict>
            </dict>
        </dict>
    </array>

To load that on the AppleTV, you can either do it the "official" way (use iPhone Configuration Utility or Configurator to load the profile via a micro-USB cable to a detatched AppleTV)...or you can do it the easy way:

1. Start up a simple web server somewhere and put the .mobileconfig file there
1. Go to the AppleTV Settings app
1. Select "General" then scroll the cursor down to highlight "Send Data To Apple"
1. Press "Play" (not the normal "Select" button)
1. Enter the URL for the .mobileconfig file (don't forget to add http://) 
1. After loading, you may need to restart the AppleTV for the change to take effect

This is much easier than the USB method.

Once you've got the Add Site button / app added, then you can add any site you like. You either need to provide a URL to a "Vendor bag" (a configuration file called bag.plist), or a URL to the app's main "home" screen (plus a name for the app). A typical bag.plist might look a little like this:


    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>menu-title</key>
        <string>My App</string>
        <key>enabled</key>
        <string>YES</string>
        <key>merchant</key>
        <string>my-app-id</string>
        <key>root-url</key>
        <string>http://my.server.com/main.xml</string>
        <key>menu-icon-url</key>
        <dict>
            <key>720</key>
            <string>http://__IP_ADDR__/images/icon720.png</string>
            <key>1080</key>
            <string>http://__IP_ADDR__/images/icon1080.png</string>
        </dict>
    </dict>
    </plist>

Several of the 3rd party apps added this year have easy-to-discover bag.plist files. You can grab one of those, change the name, point to a different icon, and load it up just to see what it does. (but see the **Caveats** section below for possible drawbacks).


## What's here

### QuickStart
Just enough to load a custom app. Includes:

* Python webserver script (just calls SimpleHTTPServer)
* addsite.mc - Mobileconfig profile that adds the Add Site button
* bag.plist - configuration to add another app
    * points to old trailers app (will that work?)
* mitm.mc - Mobileconfig profile for a wifi proxy
    * need to fill in proxy address, SSID, SSID password, etc.
    * will probably need to add certs as well
* features.mc - Mobileconfig to add a couple fun features
    * EnableFeatureEnabler - still no idea what this does
    * PrintBitRate
    * HomeSharingDiagnostics


### Simulator
This is a really ugly, horrid, terrible, dear-God-don't-use-it-seriously, and please don't judge me, hack. Basically, it's the barest of possible proxies, that just takes a request, fetches it from the distant server, and applies an XSLT transform to turn the remote server's output into HTML. The HTML is then styled with CSS and given back to the browser.

It works great for the Trailers app, okay for Vimeo and Skynews, and not at all for things like Netflix, where most of the magic happens in Javascript.

It's included here just for completeness' sake, and because I'd really love to see someone run with this and turn it into a real simulator. Ideally, it should probably be a web view in a dedicated app that can actually process the javascript and apply the XSLT transformation at the last possible moment before displaying the content. You know, just like happens on the real AppleTV.

The XSLT is rough (it's been a long while since I did anything much with XSL), and the CSS needs a lot of work. For one thing, everything should probably just be positioned absolutely, but I started off trying to make things float into place automagically and probably wasted a lot of time and effort on that. Again, I hope to see someone with actual CSS skills make this look pretty. 

I got the XSL to the point where most of the Trailers apps work pretty well (they work best in Safari, btw). The other apps -- some bits will work, some won't. There's a LOT that's simply not implemented. 

Did I mention it barely works?


### Raspberry Pi server

This is a rough hack (but not as bad as the simulator!) that starts to demonstrate how a server might work. A couple notes: 

* Getting metadata out of the videos is a pain in the neck. There just aren't many good libraries to do this, and the ones I managed to get working on the laptop I just couldn't get to work right on the Pi. 
* So you'll need to build the media database offline and then transfer it to the Raspberry Pi later. This is stupid, but it's as far as I got.
* I didn't even begin playing with advanced things like authentication, search, etc. Then again, it's just a demo.


### DerbyCon Slides

Just what it says on the tin.


## Caveats

* MITM proxying can be flaky, esp. when the ATV loads up default apps. You might need to load profile while on wired, reboot, wait for icons, then pull etheret to force all traffic thru proxy
* Adding a site (app, channel, feed, whatever) can't be reversed -- you need a factory reset to get rid of it
* Having too many sites that no longer exist (from testing, etc.) can make things flaky
* This is liable to stop working at any time, depending on Apple's whims
* All apps run as web apps within a single AppleTV binary. It's possible that information may leak between and among these apps, via javascript sandbox escapes (to read the filesystem directly), CSRF, XSS, or other dangerous acronyms.
* The logging function for Add Site is a general facility for **all** apps, not just the ones you add. It's quite chatty for some apps. It's possible some apps may even leak credentials or other sensitive information through the log, so don't point your logging URL to someone else's server.


## Acknowledgements

Thanks to my employers, Intrepidus Group, for the opportunity to dig into how all this works and the time to build it into a talk. 

Though we don't do a lot of AppleTV work, this was a great exercise in iOS reverse engineering, and hopefully the slides will help others interested in such work to better understand some of the tricks we get to use on a regular basis when reviewing iPhone and iPad applications.
