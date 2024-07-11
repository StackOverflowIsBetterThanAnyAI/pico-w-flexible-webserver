# pico_server.py or main.py

import socket
import ntptime
import time
import asyncio
from machine import Pin
from assets.colors import Colors
from memory import print_memory
from connect import connect

print_memory()

wlan, ip_address, decrypted_ssid = connect()

def log_to_file(message):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")
        
# Function to get current hour
def get_current_hour():
    try:
        ntptime.settime()
        tm = time.localtime()
        return tm[3]  # returns the hour
    except Exception as e:
        print('Could not sync time with NTP server:', e)
        log_to_file('Could not sync time with NTP server')
        return None  # Return None if time sync fails

# Load the HTML page
def get_html(html_name):
    try:
        with open(html_name, 'r') as file:
            html = file.read()
        return html
    except Exception as e:
        print('Error reading HTML file:', e)
        log_to_file(f'Error reading HTML file: {e}', e)
        return '<html><body><h1>File not found</h1></body></html>'

# HTTP start server with socket
def start_server(ports):
    for port in ports:
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reusing the port
        try:
            s.bind(addr)
            s.listen(5)  # allow multiple connections
            print('Listening on', addr)
            print('Connected to SSID:', decrypted_ssid)
            print('Connect on', 'http://{}:{}'.format(ip_address, port))
            log_to_file(f'Listening on {addr}')
            log_to_file(f'Connected to SSID {decrypted_ssid}')
            log_to_file(f'Connect on {ip_address}{port}')
            print('')
            return s
        except OSError as e:
            print(f'OSError on port {port}, trying another port.', e)
            log_to_file(f'OSError on port {port}, trying another port.' )
            log_to_file(e)
            s.close()
    return None

# Define a list of ports to try
ports_to_try = [80, 3000, 5000, 8080, 8888]

# Try to start server on one of the ports in the list
server_socket = start_server(ports_to_try)

# If all attempts fail, exit the script
if not server_socket:
    print('Failed to bind to any of the specified ports. Exiting...')
    log_to_file('Failed to bind to any of the specified ports. Exiting...')
    raise SystemExit

led = Pin('LED', Pin.OUT)
status = 'OFF'
clients = []

# Function to send updates to all connected clients
def send_update_to_clients(status):
    for client in clients[:]:
        try:
            client.send('data: {}\n\n'.format(status))
        except Exception as e:
            print('Error sending update:', e)
            log_to_file('Error sending update:')
            clients.remove(client)
            try:
                client.close()
            except Exception as e_close:
                print('Error closing client:', e_close)
                log_to_file('Error closing client:')

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

# Asynchronous function to handle SSE clients
async def handle_sse_client(client):
    while True:
        try:
            await asyncio.sleep(1)  # keep the connection alive
        except OSError:
            break

    try:
        clients.remove(client)
    except ValueError:
        pass
    client.close()

# Listening for connections
async def run_server():
    while True:
        try:
            client, addr = server_socket.accept()
            client.settimeout(60)  # Set timeout for client connections
            client_ip, client_port = addr
            print(Colors.YELLOW + f'Client IP: {client_ip}:{client_port}' + Colors.RESET)
            log_to_file( f'Client IP: {client_ip}:{client_port}')

            # receive the request
            request = client.recv(1024).decode()
            if not request:
                client.close()
                continue

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
            log_to_file(f'Connection: {connection}')
            log_to_file(f'Referer: {referer}')
            log_to_file( f'User-Agent: {user_agent}')
            print('')

            # Handle SSE connection
            if '/events' in request:
                client.send('HTTP/1.0 200 OK\r\nContent-Type: text/event-stream\r\nCache-Control: no-cache\r\nConnection: keep-alive\r\n\r\n')
                clients.append(client)
                asyncio.create_task(handle_sse_client(client))
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
                log_to_file(f'LED {status}')

            if '/led=off' in request:
                update_led('OFF')
                print(Colors.RED + f'LED {status}' + Colors.RESET)
                log_to_file(f'LED {status}')

            # Check if current time is within the allowed operating hours
            current_hour = get_current_hour()
            if current_hour is not None and (22 <= current_hour or current_hour < 6):
                print(Colors.RED + 'Server is offline between 00:00 and 08:00' + Colors.RESET)
                log_to_file('Server is offline between 00:00 and 08:00')
                response = get_html('shutdown.html')
                update_led('OFF')
            else:
                response = get_html('index.html')

            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            client.send(response.encode('utf-8'))
            client.close()
        except Exception as e:
            print('Error handling client connection:', e)
            log_to_file('Error handling client connection:')
            client.close()

try:
    asyncio.run(run_server())
except OSError as e:
    print('OSError:', e)
    log_to_file('OSError:')
except KeyboardInterrupt:
    print(Colors.RED + 'KeyboardInterrupt: Stopping server...' + Colors.RESET)
    log_to_file('KeyboardInterrupt: Stopping server...' )
finally:
    print(Colors.RED + 'Socket closed' + Colors.RESET)
    log_to_file( 'Socket closed')
    led.off()
    server_socket.close()
    for client in clients:
        try:
            client.close()
        except Exception as e:
            print('Error closing client:', e)
            log_to_file('Error closing client:')
