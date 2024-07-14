import network
import time
from lib.env_encrypted import networks, key
import rp2
import machine

def log_to_file(message):
    with open('log.txt', 'a') as f:
        f.write(f'{message}\n')

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

led = machine.Pin('LED', machine.Pin.OUT)

def connect():
    time.sleep(2)
    led.on()
    time.sleep(1)
    led.off()
    for i in range(10):
        led.on()
        time.sleep(0.25)
        led.off()
        time.sleep(0.75)
    rp2.country('DE')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(2)

    # Function to decrypt SSID and password
    def decrypt_network(network):
        decrypted_ssid = xor_encrypt_decrypt(network['ssid'], key).decode()
        decrypted_password = xor_encrypt_decrypt(network['password'], key).decode()
        return decrypted_ssid, decrypted_password

    # Scan for available networks and connect to the strongest one
    available_networks = wlan.scan()
    print('Scanning networks...')
    log_to_file('Scanning networks...')
    time.sleep(2)
    log_to_file(f'Available networks: {[net[0].decode() for net in available_networks]}')
    strongest_network = None
    max_signal_strength = -100  # Initialize with a very low value

    for network_data in networks:
        ssid, password = decrypt_network(network_data)
        if ssid in [item[0].decode() for item in available_networks]:
            time.sleep(2)
            wlan.connect(ssid, password)
            time.sleep(5)
            print('Trying to connect to', ssid)
            log_to_file(f'Trying to connect to {ssid}')
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
                led.on()
                time.sleep(1)
                led.off()
                time.sleep(2)
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
                log_to_file(f'Connected to: {decrypted_ssid}')
                log_to_file(f'IP Address: {ip_address}')
                for i in range(wlan.status()):
                    led.on()
                    time.sleep(.75)
                    led.off()
                    time.sleep(.25)

                print('Connected')
                print(wlan.ifconfig())
                log_to_file('Connected')
                log_to_file(wlan.ifconfig())
                time.sleep(2)
                return wlan, ip_address, decrypted_ssid
    else:
        print('No suitable network found.')
        log_to_file('No suitable network found.')
        led.on()
        return None, None, None
    
