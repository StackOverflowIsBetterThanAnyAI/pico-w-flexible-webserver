# execute this script in order to receive the env_encrypted.py file which is need in order to connect to a wifi

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

# Define multiple networks
networks = [
    
    {
        'ssid': b'1234567890',
        'password': b'****************',
    },
    {
        'ssid': b'0987654321',
        'password': b'****************',
    },
    {
        'ssid': b'1029384756',
        'password': b'****************',
    },
]

key = 0x55  # XOR key

# Encrypt and save the data in another file (unchanged from your original script)
encrypted_networks = []
for network in networks:
    encrypted_ssid = xor_encrypt_decrypt(network['ssid'], key)
    encrypted_password = xor_encrypt_decrypt(network['password'], key)
    encrypted_networks.append({
        'ssid': encrypted_ssid,
        'password': encrypted_password,
    })

with open('/lib/env_encrypted.py', 'w') as env_file:
    env_file.write('networks = [\n')
    for network in encrypted_networks:
        env_file.write(f'    {{\'ssid\': {network["ssid"]}, \'password\': {network["password"]}}},\n')
    env_file.write(']\n')
    env_file.write(f'key = {key}\n')
