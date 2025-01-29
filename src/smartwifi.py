import network
import socket
import time
import machine

# LED setup
led = machine.Pin("LED", machine.Pin.OUT)

def blink_led():
    while True:
        led.toggle()
        time.sleep(0.5)

def solid_led():
    led.on()

# HTML templates
def load_template(filename):
    with open(f'templates/{filename}', 'r') as f:
        return f.read()

CREDENTIALS_FORM = load_template("credentials_form.html")
LOGIN_PAGE = load_template("login_page.html")

# Wi-Fi Access Point setup
def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="PicoW-Setup", password="12345678")
    print("Access Point started: SSID='PicoW-Setup', Password='12345678'")
    while not ap.active():
        time.sleep(1)
    print("AP Ready, IP Address:", ap.ifconfig()[0])
    return ap

# Wi-Fi connection setup
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"Connecting to Wi-Fi network '{ssid}'...")
    wlan.connect(ssid, password)
    for _ in range(20):  # Wait up to 20 seconds
        if wlan.isconnected():
            print("Connected to Wi-Fi! IP Address:", wlan.ifconfig()[0])
            solid_led()
            return wlan
        time.sleep(1)
    print("Failed to connect to Wi-Fi.")
    return None

# Handle HTTP requests
def handle_request(conn):
    request = conn.recv(1024).decode()
    print("Request:", request)

    # Parse the request
    if "POST /connect" in request:
        body = request.split("\r\n\r\n")[1]
        data = {pair.split("=")[0]: pair.split("=")[1] for pair in body.split("&")}
        ssid = data.get("ssid")
        password = data.get("password")
        print(f"Received credentials: SSID={ssid}, PASSWORD={password}")
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nConnecting...")
        conn.close()
        return ssid, password

    if "POST /login" in request:
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nWelcome!")
        conn.close()
        return None, None

    if "/connect" in request:
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + CREDENTIALS_FORM)
    else:
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + LOGIN_PAGE)

    conn.close()
    return None, None

# Main function
def main():
    ap = start_ap()
    wlan = None
    
    # Start blinking LED while waiting for credentials
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
                solid_led()
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