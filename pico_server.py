from connect import connect
import socket
from machine import Pin
from assets.colors import Colors
from memory import print_memory
import ntptime
import time

print_memory()

wlan, ip_address, decrypted_ssid = connect()

# Function to get current hour
def get_current_hour():
    try:
        ntptime.settime()
    except:
        print('Could not sync time with NTP server')
    tm = time.localtime()
    return tm[3]  # returns the hour

# Check if current time is within the allowed operating hours
current_hour = get_current_hour()
if 0 == current_hour < 8:
    print(Colors.RED + 'Server is off between 00:00 and 08:00' + Colors.RESET)
    print(Colors.RED + 'Socket closed' + Colors.RESET)
    raise SystemExit('Shutting down the server during off-hours.')

# Load the HTML page
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
    return html

# HTTP start server with socket
def start_server(ports):
    for port in ports:
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        s = socket.socket()
        try:
            s.bind(addr)
            s.listen(5)  # allow multiple connections
            print('Listening on', addr)
            print('Connected to SSID:', decrypted_ssid)
            print('Connect on', 'http://{}:{}'.format(ip_address, port))
            print('')
            return s
        except OSError as e:
            print(f'OSError on port {port}, trying another port:', e)
            s.close()
    return None

# Define a list of ports to try
ports_to_try = [80, 3000, 5000, 8080, 8888]

# Try to start server on one of the ports in the list
server_socket = start_server(ports_to_try)

# If all attempts fail, exit the script
if not server_socket:
    print('Failed to bind to any of the specified ports. Exiting...')
    raise SystemExit

led = Pin('LED', Pin.OUT)
status = 'OFF'
clients = []

# Function to send updates to all connected clients
def send_update_to_clients(status):
    for client in clients:
        try:
            client.send('data: {}\n\n'.format(status))
        except Exception as e:
            print('Error sending update:', e)
            clients.remove(client)

# Update LED status and notify clients
def update_led(new_status):
    global status
    if new_status == 'ON':
        led.value(1)
        status = 'ON'
    elif new_status == 'OFF':
        led.value(0)
        status = 'OFF'
    send_update_to_clients(status)
    
# Listening for connections
try:
    while True:
        client, addr = server_socket.accept()
        client_ip, client_port = addr
        print(Colors.YELLOW + f'Client IP: {client_ip}:{client_port}' + Colors.RESET)
        
        # receive the request
        request = client.recv(1024).decode()
        
        # extract and print the User-Agent from the request headers
        user_agent = ''
        referer = ''
        connection = ''
        for line in request.split('\r\n'):
            if line.startswith('User-Agent:'):
                user_agent = line[len('User-Agent: '):]
            if line.startswith('Connection:'):
                connection = line[len('Connection: '):]
            if line.startswith('Referer:'):
                referer = line[len('Referer: '):]
        print(f'Connection: {connection}')
        print(f'Referer: {referer}')
        print(Colors.CYAN + f'User-Agent: {user_agent}' + Colors.RESET)
        print('')

        if '/events' in request:
            # Handle SSE connection
            client.send('HTTP/1.0 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\nConnection: keep-alive\r\n\r\n')
            clients.append(client)
            continue

        if '/favicon.ico' in request:
            with open('assets/favicon.ico', 'rb') as f:
                favicon = f.read()
            client.send('HTTP/1.0 200 OK\r\nContent-type: image/x-icon\r\n\r\n')
            client.send(favicon)
            client.close()
            continue
        
        if '/assets/style.css' in request:
            with open('assets/style.css', 'r') as f:
                css = f.read()
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/css\r\n\r\n')
            client.send(css.encode('utf-8'))
            client.close()
            continue
        
        if '/assets/script.js' in request:
            with open('assets/script.js', 'r') as f:
                js = f.read()
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/javascript\r\n\r\n')
            client.send(js.encode('utf-8'))
            client.close()
            continue

        if '/get_status' in request:
            client.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            client.send(f'{{"status": "{status}"}}')
            client.close()
            continue
        
        if '/led=on' in request:
            update_led('ON')
            print(Colors.GREEN + f'LED {status}' + Colors.RESET)
        
        if '/led=off' in request:
            update_led('OFF')
            print(Colors.RED + f'LED {status}' + Colors.RESET)
         
        response = get_html('index.html')
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(response.encode('utf-8'))
        client.close()
        
except OSError as e:
    print('OSError:', e)
except KeyboardInterrupt:
    print(Colors.RED + 'KeyboardInterrupt: Stopping server...' + Colors.RESET)
finally:
    print(Colors.RED + 'Socket closed' + Colors.RESET)
    led.off()
    server_socket.close()
