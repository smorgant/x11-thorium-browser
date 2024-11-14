import os
import time
import subprocess
from pyvirtualdisplay import Display
from Xlib import display as xdisplay, X

def kill_existing_virtual_display():
    """
    Kill any existing virtual displays to avoid conflicts.
    """
    try:
        output = subprocess.check_output(["pkill", "Xvfb"])
        print("Killed existing Xvfb processes.")
    except subprocess.CalledProcessError:
        print("No existing Xvfb processes found.")

def validate_window(window_name):
    """
    Check if a window with the given name exists in the X11 display.
    """
    disp = xdisplay.Display()
    root = disp.screen().root
    window_ids = root.query_tree().children

    for window_id in window_ids:
        window = disp.create_resource_object('window', window_id)
        try:
            name = window.get_wm_name()
            if name and window_name.lower() in name.lower():
                print(f"Window found: {name}")
                return True
        except X.error.BadWindow:
            # Ignore windows that can't be queried
            continue
    print(f"No window found with name '{window_name}'")
    return False

def main():
    # Define resolution
    resolution = (1920, 1080)
    width, height = resolution

    # Step 1: Kill any existing virtual displays
    kill_existing_virtual_display()

    # Step 2: Start a virtual display
    display = Display(visible=False, size=resolution)
    display.start()
    os.environ["DISPLAY"] = f":{display.display}"
    print(f"Virtual display started on {os.environ['DISPLAY']}")

    try:
        # Step 3: Launch Thorium Browser in kiosk mode
        print("Launching Thorium-browser in kiosk mode...")
        browser_proc = subprocess.Popen([
            "thorium-browser",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--kiosk",
            f"--window-size={width},{height}",
            "--start-fullscreen",
            "https://example.com"
        ])

        # Wait for the browser to launch
        time.sleep(5)

        # Step 4: Validate the Thorium browser window exists
        if not validate_window("Thorium"):
            print("Failed to validate Thorium-browser window.")
            return

        print("Thorium-browser window detected successfully.")

        # Step 5: Start the VNC server
        print("Starting VNC server...")
        vnc_proc = subprocess.Popen([
            "x11vnc",
            "-display", os.environ["DISPLAY"],
            "-forever",
            "-rfbport", "5900",
            "-nopw"
        ])

        print("VNC server started on port 5900. Connect with a VNC viewer to see the content.")

        # Keep the script running while the VNC server is active
        while vnc_proc.poll() is None:
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cleanup: Stop the virtual display and processes
        print("Cleaning up...")
        if 'browser_proc' in locals():
            browser_proc.terminate()
        if 'vnc_proc' in locals():
            vnc_proc.terminate()
        display.stop()
        print("Cleanup complete.")

if __name__ == "__main__":
    main()
