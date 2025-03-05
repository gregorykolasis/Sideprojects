import platform
import subprocess
import time
from wakeonlan import send_magic_packet

MAC_ADDRESS = 'C8-7F-54-65-F1-DF'
TARGET_HOST = '192.168.1.100'  # Change to the correct IP or hostname
MAX_ATTEMPTS = 20              # Maximum ping attempts before giving up
SLEEP_BETWEEN_PINGS = 5        # Seconds to wait between ping attempts

def is_online(host: str) -> bool:
    """
    Returns True if the host responds to a single ping, False otherwise.
    """
    # Detect current OS
    current_os = platform.system().lower()

    # Build the ping command based on OS
    if 'windows' in current_os:
        # Windows ping command: ping -n 1 -w 1000 <host>
        #   -n 1 : send 1 ping
        #   -w 1000 : timeout in milliseconds
        ping_cmd = ["ping", "-n", "1", "-w", "1000", host]
    else:
        # Unix-based ping command: ping -c 1 -W 1 <host>
        #   -c 1 : send 1 ping
        #   -W 1 : timeout in seconds
        ping_cmd = ["ping", "-c", "1", "-W", "1", host]

    try:
        subprocess.check_output(ping_cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("Ping command not found. Make sure it's installed and on your PATH.")
        return False

def main():
    print(f"Checking if {TARGET_HOST} is online...")
    
    if is_online(TARGET_HOST):
        print(f"{TARGET_HOST} is already ONLINE. No need to send WOL.")
        return
    else:
        print(f"{TARGET_HOST} is OFFLINE. Sending WOL packet to MAC: {MAC_ADDRESS}")
        try:
            send_magic_packet(MAC_ADDRESS)
        except Exception as e:
            print(f"Error {e} while sending WOL packet.")
            return

    # Now poll until the machine is online or until the maximum attempts is reached
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        time.sleep(SLEEP_BETWEEN_PINGS)
        if is_online(TARGET_HOST):
            print(f"{TARGET_HOST} is now ONLINE after {attempts+1} attempt(s).")
            break
        else:
            attempts += 1
            print(f"{TARGET_HOST} is still OFFLINE. Attempt {attempts}/{MAX_ATTEMPTS}.")

    if attempts == MAX_ATTEMPTS:
        print(f"Gave up after {MAX_ATTEMPTS} attempts. {TARGET_HOST} is still offline.")

if __name__ == "__main__":
    main()
