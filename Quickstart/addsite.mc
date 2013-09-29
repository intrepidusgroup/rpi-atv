
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
    <string>494E5452-4550-4944-5553-000000000001</string>
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
            <string>494E5452-4550-4944-5553-000000000002</string>
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
<!-- you'll need to fix the URL below -->
                            <string>http://__IP_ADDR__/log</string>
                        </dict>
                    </dict>
                </dict>
            </array>
        </dict>
    </array>
</dict>
</plist>
