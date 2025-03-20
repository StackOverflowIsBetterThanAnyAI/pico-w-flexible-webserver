# Raspberry Pi Pico W flexible Webserver

1. Open the Thonny IDE

2. Clone your files to your Raspberry Pi Pico W.

3. To ensure that everything works flawlessly, please check, that you have the wireless Pico version.
 
4. Set your Wifi details in `env.py`: You can add <b>as many access points</b> as you want.

```
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
```

6. Run the `env.py` script in order to generate the `env_encrypted.py` file with your encrypted WiFi data.

7. In order to check for full functionality, execute the `pico_server.py` script manually inside your Thonny IDE.

8. To detect the IP address of your future webserver, you can either look into your WiFi settings or start the `pico_server.py` script manually.

9. If your Pico W successfully connects to one of your access points and returns an IP address with its port, everything has worked. If so, feel free to rename `pico_server.py` to `main.py`.

10. This ensures that if you unplug your Raspberry Pi Pico W and plug it in again, the `main.py` script is executed automatically on start.

11. Because the automatically executed file takes a lot longer, I have added a couple of `time.sleep(x)` commands in the `connect.py` file. If you execute the script manually, feel free to remove these lines.

12. If everything runs correctly, the onboard LED should flash for one second and blink faster another nine times.

13. Give your Pico at least ten seconds (because of a couple `time.sleep(x)` statements) and the LED will flash once more if it connects to one of your specified access points.

14. If the onboard LED blinks another three times, you are ready to go. Everything has worked flawlessly and you can now connect to your webserver with the previously gathered IP address.

15. If the LED instead turns on and never goes out, an error has occured.

16. If problems occur, check the automatically generated `log.txt` file, which will help you start debugging.

17. You can connect multiple devices to this webserver. Depending on the time, you wil either receive a html file which says that the server is currently offline or a file which lets you control the onboard LED.

```
current_hour = get_current_hour()
if current_hour is not None and (22 <= current_hour or current_hour < 6):
    print(Colors.RED + 'Server is offline between 00:00 and 08:00' + Colors.RESET)
    log_to_file('Server is offline between 00:00 and 08:00')
    response = get_html('shutdown.html')
    update_led('OFF')
else:
    response = get_html('index.html')
```

19. As already mentioned, you are allowed to use multiple devices. Because of <b>SSE (Server Sent Events)</b>, the UI will update on all devices depending on the current LED state.

20. I hope that this (more or less) simple project gives you an idea of how you can utilize your Raspberry Pi Pico W for your use case.
