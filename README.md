# Raspberry Pi Pico W flexible Webserver

1. Open the Thonny IDE

2. Clone your files to your Raspberry Pi Pico W.

3. To ensure that everything works flawlessly, please ensure, that you have the wireless Pico version.
 
4. Set your Wifi details in `env.py`: You can add <b>as many access points</b> as you want.

5. Run the `env.py` script in order to generate the `env_encrypted.py` file with your encrypted wifi data.

6. In order to check for full functionality, execute the `pico_server.py` script manually inside your Thonny IDE.

7. In order to detect the IP address of your future webserver, you can either look into your wifi settings or start the `pico_server.py` script manually.

8. If your Pico W successfully connects to one of your access points and returns an IP address with its port, everything has worked. If so, feel free to rename `pico_server.py` to `main.py`.

9. This ensures that if you unplug your Raspberry Pi Pico W and plug it in again, the `main.py` script is executed automatically.

10. Because the automatically executed file takes a lot longer, I have added a couple of `time.sleep(x)` commands in the `connect.py` file. If you execute the script manually, feel free to remove these lines.

11. If everything runs correctly, the onboard LED should flash for one second and blink faster another nine times.

12. Give your Pico at least ten seconds (because of a couple `time.sleep(x)` statements) and the LED will flash once more if it connects to one of your specified access points.

13. If the LED blinks another three times, you are ready to go. Everything has worked flawlessly and you can now connect to your webserver.

14. You can connect multiple devices to this webserver. Depending on the time, you wil either receive a html file which says that the server is currently offline or a file which lets you control the onboard LED.

15. As already mentioned, you are allowed to use multiple devices. Because of SSE (Server Sent Events), the UI will update on all devices depending on the current LED state.

16. I hope that this (more or less) simple project gives you an idea of how you can utilize your Raspberry Pi Pico W for your use case.
