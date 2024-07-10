import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Scanning for WiFi networks
scan_results = wlan.scan()

# Results sorted by the RSSI value
sorted_results = sorted(scan_results, key=lambda x: x[3], reverse=True)

# Print the header
print('{:<40} {:<40} {:<10} {:<10}'.format('SSID', 'BSSID', 'RSSI', 'Security'))

# Print the sorted and formatted wifi networks
for element in sorted_results:
    ssid = element[0].decode('utf-8') 
    bssid = ':'.join('%02x' % b for b in element[1])
    rssi = element[3]
    security = element[4]
    
    print('{:<30} {:<30} {:<15} {:<10}'.format(ssid, bssid, rssi, security))
    
