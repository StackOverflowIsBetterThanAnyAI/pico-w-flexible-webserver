import network
import time
from lib.env_encrypted import networks, key
import rp2
import machine

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

def connect():
    rp2.country('DE')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Function to decrypt SSID and password
    def decrypt_network(network):
        decrypted_ssid = xor_encrypt_decrypt(network['ssid'], key).decode()
        decrypted_password = xor_encrypt_decrypt(network['password'], key).decode()
        return decrypted_ssid, decrypted_password

    # Scan for available networks and connect to the strongest one
    available_networks = wlan.scan()
    print('Scanning networks...')
    strongest_network = None
    max_signal_strength = -100  # Initialize with a very low value

    for network_data in networks:
        ssid, password = decrypt_network(network_data)
        if ssid in [item[0].decode() for item in available_networks]:
            wlan.connect(ssid, password)
            print('Trying to connect to', ssid)
            time.sleep(5)  # Wait for connection to establish
            
            # Handle connection error
            # Error meanings
            # 0 Link Down
            # 1 Link Join
            # 2 Link NoIp
            # 3 Link Up
            # -1 Link Fail
            # -2 Link NoNet
            # -3 Link BadAuth

            if wlan.isconnected():
                signal_strength = wlan.status('rssi')
                if signal_strength > max_signal_strength:
                    max_signal_strength = signal_strength
                    strongest_network = network_data

            wlan.disconnect()

    if strongest_network:
        decrypted_ssid, decrypted_password = decrypt_network(strongest_network)
        wlan.connect(decrypted_ssid, decrypted_password)
        time.sleep(5)  # Wait for connection to establish

        if wlan.isconnected():
            ip_address = wlan.ifconfig()[0]
            if ip_address != '0.0.0.0':
                print('Connected to:', decrypted_ssid)
                print('IP Address:', ip_address)
                led = machine.Pin('LED', machine.Pin.OUT)
                for i in range(wlan.status()):
                    led.on()
                    time.sleep(.75)
                    led.off()
                    time.sleep(.25)

                print('Connected')
                print(wlan.ifconfig())
                return wlan, ip_address, decrypted_ssid
    else:
        print('No suitable network found.')
        return None, None, None
    
