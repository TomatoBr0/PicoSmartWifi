import network
import socket
import time
import machine
from smartwifi import start_ap, connect_to_wifi, handle_request

# Main function
def main():
    ap = start_ap()
    wlan = None
    
    # Start blinking LED while waiting for credentials
    led = machine.Pin("LED", machine.Pin.OUT)
    led_thread = machine.Timer(period=500, mode=machine.Timer.PERIODIC, callback=lambda t: led.toggle())

    # Set up a socket for handling HTTP requests
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)

    while True:
        conn, addr = s.accept()
        print("Client connected from", addr)

        ssid, password = handle_request(conn)

        # If Wi-Fi credentials are received, try connecting
        if ssid and password:
            wlan = connect_to_wifi(ssid, password)
            if wlan and wlan.isconnected():
                led_thread.deinit()  # Stop blinking LED
                led.on()
                break

    # Switch to STA mode and stop AP
    ap.active(False)
    print("Access Point stopped.")

    # Restart socket for login page
    s.close()
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Serving login page on", wlan.ifconfig()[0])

    # Serve login page
    while True:
        conn, addr = s.accept()
        print("Client connected from", addr)
        handle_request(conn)

# Run the main program
if __name__ == "__main__":
    main()