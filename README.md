# pico-wifi-project/pico-wifi-project/README.md

# Pico Wi-Fi Project

This project sets up a Wi-Fi access point on the Raspberry Pi Pico W and allows users to connect to an existing Wi-Fi network. It provides a simple web interface for users to input their Wi-Fi credentials and manage access.

## Project Structure

```
pico-wifi-project
├── src
│   ├── main.py                # Entry point of the application
│   ├── smartwifi.py           # Core functionality for Wi-Fi management
│   └── templates
│       ├── credentials_form.html  # HTML form for Wi-Fi credentials
│       └── login_page.html        # HTML form for user login
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd pico-wifi-project
   ```

2. **Install dependencies**:
   Ensure you have the required libraries installed. You can list them in `requirements.txt` and install them as needed.

3. **Upload to Raspberry Pi Pico W**:
   Use your preferred method to upload the contents of the `src` directory to your Raspberry Pi Pico W.

4. **Run the application**:
   Execute `main.py` on the Pico W to start the access point and serve the web interface.

## Usage Guidelines

- Connect to the Wi-Fi network named `PicoW-Setup` using the password `12345678`.
- Open a web browser and navigate to the IP address of the Pico W to access the configuration page.
- Enter your existing Wi-Fi credentials to connect to the internet.

## Additional Information

For any issues or contributions, please refer to the project's issue tracker or contact the maintainer.