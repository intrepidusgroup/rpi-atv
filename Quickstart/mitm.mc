<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>PayloadContent</key>
	<array>
		<dict>
			<key>AutoJoin</key>
			<true/>
			<key>EncryptionType</key>
			<string>Any</string>
			<key>HIDDEN_NETWORK</key>
			<false/>
			<key>Password</key>
<!-- WiFi password goes next -->
			<string>MyPasswordIsFullOfEels</string>
			<key>PayloadDescription</key>
			<string>Configures wireless connectivity settings.</string>
			<key>PayloadDisplayName</key>
			<string>MITM Proxy Config</string>
			<key>PayloadIdentifier</key>
			<string>com.ig.burpproxy.</string>
			<key>PayloadOrganization</key>
			<string></string>
			<key>PayloadType</key>
			<string>com.apple.wifi.managed</string>
			<key>PayloadUUID</key>
			<string>494E5452-4550-4944-5553-000000000005</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
<!-- change your proxy server and port -->
			<key>ProxyServer</key>
			<string>10.11.12.13</string>
			<key>ProxyServerPort</key>
			<integer>8080</integer>
			<key>ProxyType</key>
			<string>Manual</string>
<!-- and your WiFi SSID -->
			<key>SSID_STR</key>
			<string>Linksys</string>
		</dict>
		<dict>
<!-- you can add certificates for your proxy too, but it's complicated. 
Might be easiest just to create these as profiles via iPhone Configuration
Utility and add them separately. -->
			<key>PayloadCertificateFileName</key>
			<string>PortSwiggerCA-1.5.12.cer</string>
			<key>PayloadContent</key>
			<data>
<!-- big block of b64 data goes here.... -->
                LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN4RENDQWky
                Z0F3SUJBZ0lFVDlqdE9EQU5CZ2txaGtpRzl3MEJBUVVGQURDQmlq
<!-- .... -->
                RS0tLS0tCg==
			</data>
			<key>PayloadDescription</key>
			<string>Provides device authentication (certificate or identity).</string>
			<key>PayloadDisplayName</key>
			<string>PortSwigger CA 1.5.12</string>
			<key>PayloadIdentifier</key>
			<string>com.ig.burp.cert</string>
			<key>PayloadOrganization</key>
			<string></string>
			<key>PayloadType</key>
			<string>com.apple.security.root</string>
			<key>PayloadUUID</key>
			<string>494E5452-4550-4944-5553-000000000006</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
		</dict>
	</array>
	<key>PayloadDescription</key>
	<string>Wifi profile with burp proxy</string>
	<key>PayloadDisplayName</key>
	<string>WiFi Proxy</string>
	<key>PayloadIdentifier</key>
	<string>com.ig.wifiburp</string>
	<key>PayloadOrganization</key>
	<string></string>
	<key>PayloadRemovalDisallowed</key>
	<false/>
	<key>PayloadType</key>
	<string>Configuration</string>
	<key>PayloadUUID</key>
	<string>494E5452-4550-4944-5553-000000000007</string>
	<key>PayloadVersion</key>
	<integer>1</integer>
</dict>
</plist>
