# execute this script in order to receive the env_encrypted.py file which is need in order to connect to a wifi

def xor_encrypt_decrypt(data, key):
    return bytearray([b ^ key for b in data])

# access data
ssid = b"123-456-789-0"
password = b"****************"
key = 0x55  # XOR key

# encrypting
encrypted_ssid = xor_encrypt_decrypt(ssid, key)
encrypted_password = xor_encrypt_decrypt(password, key)

# save the encrypted data in another file
with open("/lib/env_encrypted.py", "w") as env_file:
    env_file.write(f"ssid = {encrypted_ssid}\n")
    env_file.write(f"password = {encrypted_password}\n")
    env_file.write(f"key = {key}\n")
