# Streaming Thorium Browser via VNC

This project provides a simple solution for deploying and streaming a Thorium-browser session in kiosk mode via VNC. It sets up a virtual X11 display using Xvfb, streams the display using x11vnc, and ensures compatibility with headless Linux environments. Ideal for showcasing web content in fullscreen remotely.

---

## Prerequisites

### System Requirements
- Ubuntu Linux (tested on 20.04 and later)
- Internet access (to download necessary packages)

### Required Packages
1. Install required system packages:
    ```bash
    sudo apt update
    sudo apt install -y xvfb x11vnc thorium-browser python3-pip
    ```

2. Install required Python libraries:
    ```bash
    pip3 install pyvirtualdisplay python-xlib
    ```

---

## Deployment Steps

1. **Clone or Copy the Python Script**
    Clone this repository or copy the provided Python script (`vnc_thorium_stream.py`) to your Ubuntu machine.

    Example command to clone the repository:
    ```bash
    git clone https://github.com/your-repo/vnc-thorium-stream.git
    cd vnc-thorium-stream
    ```

2. **Make the Script Executable**
    Navigate to the directory containing the script and ensure it is executable:
    ```bash
    chmod +x vnc_thorium_stream.py
    ```

3. **Run the Script**
    Execute the script to start the virtual display, launch Thorium-browser in kiosk mode, and set up the VNC server:
    ```bash
    python3 vnc_thorium_stream.py
    ```

4. **Connect via VNC Viewer**
    - Use a VNC viewer (e.g., RealVNC, TigerVNC, or any preferred client) to connect to the machine.
    - Enter the IP address of the machine and port `5900` (e.g., `192.168.1.100:5900`).

    The browser content should be visible on the VNC client.

---

## Configuration Details

### Script Overview
- **Virtual Display**:
    - `Xvfb` is used to create a virtual X11 display (`:0`).
    - Resolution is set to 1920x1080.

- **Thorium Browser**:
    - Launched in kiosk mode (`--kiosk`) and fullscreen.
    - Default URL is set to `https://example.com`. You can change this in the script by editing:
        ```python
        "https://example.com"
        ```

- **VNC Server**:
    - `x11vnc` streams the virtual display on port `5900`.

### Changing Resolution
To adjust the resolution, update the `resolution` variable in the script:
```python
resolution = (1920, 1080)
```

### Changing the Browser URL
Modify the URL passed to Thorium-browser in the script:
```python
"https://example.com"
```

## Troubleshooting

### Common Issues
1. **Black Screen in VNC Viewer**:
    - Ensure the script is running.
    - Verify `Xvfb` is active:
        ```bash
        ps aux | grep Xvfb
        ```
    - Check if `x11vnc` is running:
        ```bash
        ps aux | grep x11vnc
        ```

2. **Connection Refused on VNC**:
    - Confirm port `5900` is open on the machine:
        ```bash
        sudo ss -tuln | grep 5900
        ```
    - Ensure no firewall is blocking the port.

3. **Browser Not Launching**:
    - Verify Thorium-browser is installed correctly by running:
        ```bash
        thorium-browser --version
        ```

### Logs and Debugging
- The script logs important events to the terminal.
- Check for error messages and use them to identify issues.

---

## Uninstall Instructions

To remove the setup:
1. Stop any running instances:
    ```bash
    pkill -f vnc_thorium_stream.py
    pkill -f Xvfb
    pkill -f x11vnc
    ```

2. Optionally, remove installed packages:
    ```bash
    sudo apt remove --purge -y xvfb x11vnc thorium-browser
    sudo apt autoremove -y
    ```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
