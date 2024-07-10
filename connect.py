import network
import time
from lib.env_encrypted import ssid, password, key
import rp2
import machine

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

# decrypting
decrypted_ssid = xor_encrypt_decrypt(ssid, key).decode()
decrypted_password = xor_encrypt_decrypt(password, key).decode()

def connect():
    rp2.country("DE")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    while True:
        wlan.connect(decrypted_ssid, decrypted_password)
        
        # Handle connection error
        # Error meanings
        # 0 Link Down
        # 1 Link Join
        # 2 Link NoIp
        # 3 Link Up
        # -1 Link Fail
        # -2 Link NoNet
        # -3 Link BadAuth
        
        while not wlan.isconnected() and wlan.status() >= 0 and wlan.status() != 3:
            print("Waiting for connection...")
            time.sleep(1)
            
        if wlan.status() == 3:
            ip_address = wlan.ifconfig()[0]
            if ip_address != '0.0.0.0':
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
                print("Invalid IP address. Reconnecting...")
                wlan.disconnect()
                time.sleep(2)
                continue
        else:
            print("Connection failed with status:", wlan.status())
            wlan.disconnect()
            time.sleep(2)
            continue

if __name__ == "__main__":
    wlan, ip_address, decrypted_ssid = connect()

