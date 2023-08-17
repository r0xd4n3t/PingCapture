import os
import subprocess
import argparse
import pyautogui
import time
from datetime import datetime

# Define color codes for console output
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_FORMAT = "\033[0m"

# Define the output folder for screenshots and ping logs
output_folder = "ping_results"

def clear_console():
    try:
        # Clear the console screen based on the operating system
        os.system('clear' if os.name == 'posix' else 'cls')
    except Exception as e:
        print("Error clearing the console:", e)

def run_ping(host, count):
    try:
        # Run the ping command and capture the output
        ping_command = ["ping", "-c" if os.name != "nt" else "-n", str(count), host]
        output = subprocess.check_output(ping_command, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e.output)

def capture_screenshot(filename):
    try:
        # Delay to ensure the console output is visible
        time.sleep(1)

        # Capture the entire screen and save the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print("Error capturing screenshot:", e)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Ping targets from a list and capture screenshots.")
    parser.add_argument("-f", "--file", required=True, help="File containing a list of IP addresses")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests (default: 4)")
    args = parser.parse_args()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the list of IP addresses from the file
    with open(args.file, "r") as file:
        ip_list = file.read().splitlines()

    print("Ping results:")
    clear_console()
    
    # Ping each target, capture a screenshot, and save the ping log
    for idx, ip in enumerate(ip_list, start=1):  # Use enumerate with start to improve readability
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Current time: {current_time}")
            print(f"\n{COLOR_GREEN}Target {idx}/{len(ip_list)}: {ip}{COLOR_RESET}")
            ping_result = run_ping(ip, args.count)

            print(f"\nResult:")
            formatted_ping_result = "\n".join([f"{COLOR_RED}{line}{COLOR_RESET}" for line in ping_result.split("\n")])
            print(formatted_ping_result)

            log_filename = os.path.join(output_folder, f"ping_log_{idx}.txt")
            with open(log_filename, "w") as log_file:
                log_file.write(ping_result)

            screenshot_filename = os.path.join(output_folder, f"ping_screenshot_{idx}.png")
            capture_screenshot(screenshot_filename)

        except Exception as e:
            print("Error processing target:", e)
        
        clear_console()

if __name__ == "__main__":
    main()
